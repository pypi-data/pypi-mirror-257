from .. import version
from ..pipeline.config import parse_nabu_config_file
from ..pipeline.config_validators import convert_to_int
from .cli_configs import ReconstructConfig
from .utils import parse_params_values


def update_reconstruction_start_end(conf_dict, user_indices):
    if len(user_indices) == 0:
        return
    rec_cfg = conf_dict["reconstruction"]
    err = None

    val_int, conv_err = convert_to_int(user_indices)
    if conv_err is None:
        start_z = user_indices
        end_z = user_indices
    else:
        if user_indices in ["first", "middle", "last"]:
            start_z = user_indices
            end_z = user_indices
        elif user_indices == "all":
            start_z = 0
            end_z = -1
        elif "-" in user_indices:
            try:
                start_z, end_z = user_indices.split("-")
                start_z = int(start_z)
                end_z = int(end_z)
            except Exception as exc:
                err = "Could not interpret slice indices '%s': %s" % (user_indices, str(exc))
        else:
            err = "Could not interpret slice indices: %s" % user_indices
        if err is not None:
            print(err)
            exit(1)
    rec_cfg["start_z"] = start_z
    rec_cfg["end_z"] = end_z


def get_log_file(arg_logfile, legacy_arg_logfile, forbidden=None):
    default_arg_val = ""
    # Compat. log_file --> logfile
    if legacy_arg_logfile != default_arg_val:
        logfile = legacy_arg_logfile
    else:
        logfile = arg_logfile
    #
    if forbidden is None:
        forbidden = []
    for forbidden_val in forbidden:
        if logfile == forbidden_val:
            print("Error: --logfile argument cannot have the value %s" % forbidden_val)
            exit(1)
    if logfile == "":
        logfile = True
    return logfile


def get_reconstructor(args, overwrite_options=None):
    # Imports are done here, otherwise "nabu --version" takes forever
    from ..pipeline.fullfield.processconfig import ProcessConfig
    from ..pipeline.fullfield.reconstruction import FullFieldReconstructor

    #

    # A crash with scikit-cuda happens only on PPC64 platform if and nvidia-persistenced is running.
    # On such machines, a warm-up has to be done.
    import platform

    if platform.machine() == "ppc64le":
        try:
            from silx.math.fft.cufft import CUFFT
        except:  # can't catch narrower - cublasNotInitialized requires cublas !
            CUFFT = None
    #

    logfile = get_log_file(args["logfile"], args["log_file"], forbidden=[args["input_file"]])
    conf_dict = parse_nabu_config_file(args["input_file"])
    update_reconstruction_start_end(conf_dict, args["slice"].strip())
    if overwrite_options is not None:
        for option_key, option_val in overwrite_options.items():
            opt_section, opt_name = option_key.split("/")
            conf_dict[opt_section][opt_name] = option_val

    proc = ProcessConfig(conf_dict=conf_dict, create_logger=logfile)
    logger = proc.logger

    logger.info("Going to reconstruct slices (%d, %d)" % (proc.rec_region["start_z"], proc.rec_region["end_z"]))

    # Get extra options
    extra_options = {
        "gpu_mem_fraction": args["gpu_mem_fraction"],
        "cpu_mem_fraction": args["cpu_mem_fraction"],
        "chunk_size": args["max_chunk_size"] if args["max_chunk_size"] > 0 else None,
        "margin": args["phase_margin"],
        "force_grouped_mode": bool(args["force_use_grouped_pipeline"]),
    }

    reconstructor = FullFieldReconstructor(proc, logger=logger, extra_options=extra_options)
    return reconstructor


def main():
    args = parse_params_values(
        ReconstructConfig,
        parser_description=f"Perform a tomographic reconstruction.",
        program_version="nabu " + version,
    )

    R = get_reconstructor(args)
    proc = R.process_config

    R.reconstruct()
    R.finalize_files_saving()
    return 0


if __name__ == "__main__":
    main()
