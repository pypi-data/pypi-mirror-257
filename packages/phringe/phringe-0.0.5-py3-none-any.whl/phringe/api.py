import shutil
from datetime import datetime
from pathlib import Path

import numpy as np

from phringe.core.entities.observation import Observation
from phringe.core.entities.observatory.observatory import Observatory
from phringe.core.entities.scene import Scene
from phringe.core.entities.settings import Settings
from phringe.core.processing.data_generator import DataGenerator
from phringe.io.fits_writer import FITSWriter
from phringe.io.txt_reader import TXTReader
from phringe.io.yaml_handler import YAMLHandler


class API:
    """Class representation of the API."""

    @staticmethod
    def generate_data(
            config_file_path_or_dict,
            exoplanetary_system_file_path_or_dict,
            spectrum_file_path=None,
            output_dir=Path('.'),
            fits=True,
            copy=True
    ) -> np.ndarray:
        """Generate synthetic photometry data.

        :param config_file_path_or_dict: The path to the configuration file or the configuration dictionary
        :param exoplanetary_system_file_path_or_dict: The path to the exoplanetary system file or the exoplanetary system dictionary
        :param spectrum_file_path: The path to the spectrum file
        :param output_dir: The output directory
        :param fits: Whether to write the data to a FITS file
        :param copy: Whether to copy the input files to the output directory
        :return: The data
        """

        try:
            config_file_path_or_dict = Path(config_file_path_or_dict)
            config_dict = YAMLHandler().read(config_file_path_or_dict)
        except TypeError:
            config_dict = config_file_path_or_dict
        try:
            exoplanetary_system_file_path_or_dict = Path(exoplanetary_system_file_path_or_dict)
            system_dict = YAMLHandler().read(exoplanetary_system_file_path_or_dict)
        except TypeError:
            system_dict = exoplanetary_system_file_path_or_dict
        try:
            spectrum_file_path = Path(spectrum_file_path)
        except TypeError:
            pass
        try:
            output_dir = Path(output_dir)
            planet_spectrum = TXTReader().read(spectrum_file_path) if spectrum_file_path else None
        except TypeError:
            pass

        settings = Settings(**config_dict['settings'])
        observation = Observation(**config_dict['observation'])
        observatory = Observatory(**config_dict['observatory'])
        scene = Scene(**system_dict)

        settings.prepare(observation, observatory)
        observation.prepare()
        observatory.prepare(settings, observation, scene)
        scene.prepare(settings, observatory, planet_spectrum)

        data_generator = DataGenerator(settings=settings, observation=observation, observatory=observatory, scene=scene)
        data = data_generator.run()

        # If any output files should be written, create the data directory in the output directory
        if fits or copy:
            output_dir = output_dir.joinpath(f'out_{datetime.now().strftime("%Y%m%d_%H%M%S.%f")}')
            output_dir.mkdir(parents=True, exist_ok=True)

        if fits:
            fits_writer = FITSWriter().write(data, output_dir)

        if copy:
            if isinstance(config_file_path_or_dict, Path):
                shutil.copy(config_file_path_or_dict, output_dir.joinpath(config_file_path_or_dict.name))
            else:
                YAMLHandler().write(config_file_path_or_dict, output_dir.joinpath('config.yaml'))
            if isinstance(exoplanetary_system_file_path_or_dict, Path):
                shutil.copy(
                    exoplanetary_system_file_path_or_dict,
                    output_dir.joinpath(exoplanetary_system_file_path_or_dict.name)
                )
            else:
                YAMLHandler().write(exoplanetary_system_file_path_or_dict, output_dir.joinpath('system.yaml'))

        return data
