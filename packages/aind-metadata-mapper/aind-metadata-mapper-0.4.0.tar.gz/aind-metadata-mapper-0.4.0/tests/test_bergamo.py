"""Tests parsing of session information from bergamo rig."""

import gzip
import json
import os
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from aind_data_schema.core.session import Session

from aind_metadata_mapper.bergamo.session import (
    BergamoEtl,
    RawImageInfo,
    UserSettings,
)

RESOURCES_DIR = (
    Path(os.path.dirname(os.path.realpath(__file__))) / "resources" / "bergamo"
)
EXAMPLE_MD_PATH = RESOURCES_DIR / "example_metadata.txt.gz"
EXAMPLE_DES_PATH = RESOURCES_DIR / "example_description0.txt"
EXAMPLE_IMG_PATH = RESOURCES_DIR / "cropped_neuron50_00001.tif"
EXPECTED_SESSION = RESOURCES_DIR / "expected_session.json"


class TestBergamoEtl(unittest.TestCase):
    """Test methods in BergamoEtl class."""

    @classmethod
    def setUpClass(cls):
        """Load record object and user settings before running tests."""
        with gzip.open(EXAMPLE_MD_PATH, "rt") as f:
            raw_md_contents = f.read()
        with open(EXAMPLE_DES_PATH, "r") as f:
            raw_des0_contents = f.read()
        with open(EXPECTED_SESSION, "r") as f:
            expected_session_contents = json.load(f)
        cls.example_metadata = raw_md_contents
        cls.example_description0 = raw_des0_contents
        cls.example_shape = [347, 512, 512]
        cls.example_user_settings = UserSettings(
            mouse_platform_name="some_mouse_platform_name",
            active_mouse_platform=True,
            experimenter_full_name=["John Smith", "Jane Smith"],
            subject_id="12345",
            session_start_time=datetime(2023, 10, 10, 14, 0, 0),
            session_end_time=datetime(2023, 10, 10, 17, 0, 0),
            stream_start_time=datetime(2023, 10, 10, 15, 0, 0),
            stream_end_time=datetime(2023, 10, 10, 16, 0, 0),
            stimulus_start_time=datetime(2023, 10, 10, 15, 15, 0),
            stimulus_end_time=datetime(2023, 10, 10, 15, 45, 0),
        )
        cls.expected_session = expected_session_contents

    @patch("aind_metadata_mapper.bergamo.session.ScanImageTiffReader")
    def test_extract(self, mock_reader: MagicMock):
        """Tests that the raw image info is extracted correcetly."""
        mock_context = mock_reader.return_value.__enter__.return_value
        mock_context.metadata.return_value = self.example_metadata
        mock_context.description.return_value = self.example_description0
        mock_context.shape.return_value = self.example_shape
        # Test extracting where input source is a directory
        etl_job1 = BergamoEtl(
            input_source=RESOURCES_DIR,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        raw_image_info1 = etl_job1._extract()
        self.assertEqual(2310025, len(raw_image_info1.metadata))
        self.assertEqual(2000, len(raw_image_info1.description0))
        self.assertEqual([347, 512, 512], raw_image_info1.shape)

        # Test extracting where input source is a file
        etl_job2 = BergamoEtl(
            input_source=EXAMPLE_IMG_PATH,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        raw_image_info2 = etl_job2._extract()
        self.assertEqual(2310025, len(raw_image_info2.metadata))
        self.assertEqual(2000, len(raw_image_info2.description0))
        self.assertEqual([347, 512, 512], raw_image_info2.shape)

        # Test extracting where input source is a str
        etl_job3 = BergamoEtl(
            input_source=str(EXAMPLE_IMG_PATH),
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        raw_image_info3 = etl_job3._extract()
        self.assertEqual(2310025, len(raw_image_info3.metadata))
        self.assertEqual(2000, len(raw_image_info3.description0))
        self.assertEqual([347, 512, 512], raw_image_info3.shape)

        # Test error is raised if no tif file in dir
        etl_job4 = BergamoEtl(
            input_source=str(RESOURCES_DIR / ".."),
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        with self.assertRaises(FileNotFoundError) as e:
            etl_job4._extract()
        self.assertEqual(
            "Directory must contain tif or tiff file!", str(e.exception)
        )

    def test_flat_dict_to_nested(self):
        """Test util method to convert dictionaries from flat to nested."""
        original_input = {
            "SI.LINE_FORMAT_VERSION": 1,
            "SI.VERSION_UPDATE": 0,
            "SI.acqState": "loop",
            "SI.acqsPerLoop": "10000",
            "SI.errorMsg": "",
            "SI.extTrigEnable": "1",
            "SI.fieldCurvatureRxs": "[]",
            "SI.fieldCurvatureZs": "[]",
            "SI.hBeams.enablePowerBox": "false",
            "SI.hBeams.errorMsg": "",
            "SI.hBeams.lengthConstants": "[200 Inf]",
            "SI.hBeams.name": "SI Beams",
        }

        expected_output = {
            "SI": {
                "LINE_FORMAT_VERSION": 1,
                "VERSION_UPDATE": 0,
                "acqState": "loop",
                "acqsPerLoop": "10000",
                "errorMsg": "",
                "extTrigEnable": "1",
                "fieldCurvatureRxs": "[]",
                "fieldCurvatureZs": "[]",
                "hBeams": {
                    "enablePowerBox": "false",
                    "errorMsg": "",
                    "lengthConstants": "[200 Inf]",
                    "name": "SI Beams",
                },
            }
        }

        actual_output = BergamoEtl._flat_dict_to_nested(original_input)
        self.assertEqual(expected_output, actual_output)

    @patch("logging.error")
    def test_parse_raw_image_info(self, mock_log: MagicMock):
        """Tests that raw image info is parsed correctly."""
        raw_image_info = RawImageInfo(
            metadata=self.example_metadata,
            description0=self.example_description0,
            shape=self.example_shape,
        )

        etl_job1 = BergamoEtl(
            input_source=RESOURCES_DIR,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        actual_parsed_data = etl_job1._parse_raw_image_info(raw_image_info)
        mock_log.assert_called_once_with(
            "Multiple planes not handled in metadata collection. "
            "HANDLE ME!!!: KeyError('userZs')"
        )
        self.assertEqual([347, 512, 512], actual_parsed_data.shape)
        self.assertEqual(1, actual_parsed_data.num_planes)
        self.assertEqual(
            datetime(2023, 7, 24, 14, 14, 17, 854000),
            actual_parsed_data.movie_start_time,
        )
        self.assertEqual("30.0119", actual_parsed_data.frame_rate)
        self.assertEqual(
            {"fs": "30.0119", "nplanes": 1, "nrois": 1, "mesoscan": 0},
            actual_parsed_data.roi_data,
        )
        self.assertEqual(
            "1", actual_parsed_data.description_first_frame["frameNumbers"]
        )
        self.assertEqual(
            "false", actual_parsed_data.metadata["hBeams"]["enablePowerBox"]
        )
        self.assertEqual(
            "1", actual_parsed_data.metadata["LINE_FORMAT_VERSION"]
        )

    @patch("logging.error")
    def test_transform(self, mock_log: MagicMock):
        """Tests raw image info is parsed into a Session object correctly"""
        raw_image_info = RawImageInfo(
            metadata=self.example_metadata,
            description0=self.example_description0,
            shape=self.example_shape,
        )

        etl_job1 = BergamoEtl(
            input_source=RESOURCES_DIR,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        actual_session = etl_job1._transform(raw_image_info)
        self.assertEqual(
            self.expected_session, json.loads(actual_session.model_dump_json())
        )
        mock_log.assert_called_once_with(
            "Multiple planes not handled in metadata collection. "
            "HANDLE ME!!!: KeyError('userZs')"
        )

    @patch("aind_data_schema.base.AindCoreModel.write_standard_file")
    @patch("aind_metadata_mapper.bergamo.session.ScanImageTiffReader")
    @patch("logging.error")
    @patch("logging.debug")
    def test_run_job(
        self,
        mock_log_debug: MagicMock,
        mock_log_error: MagicMock,
        mock_reader: MagicMock,
        mock_file_write: MagicMock,
    ):
        """Tests run_job command"""
        mock_context = mock_reader.return_value.__enter__.return_value
        mock_context.metadata.return_value = self.example_metadata
        mock_context.description.return_value = self.example_description0
        mock_context.shape.return_value = self.example_shape
        etl_job = BergamoEtl(
            input_source=RESOURCES_DIR,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        etl_job.run_job()
        mock_file_write.assert_called_once_with(output_directory=RESOURCES_DIR)
        mock_log_error.assert_called_once_with(
            "Multiple planes not handled in metadata collection. "
            "HANDLE ME!!!: KeyError('userZs')"
        )
        mock_log_debug.assert_called_once_with(
            "No validation errors detected."
        )

    @patch("aind_data_schema.base.AindCoreModel.write_standard_file")
    @patch("aind_metadata_mapper.bergamo.session.ScanImageTiffReader")
    @patch("logging.error")
    @patch("logging.debug")
    def test_run_job_write_error(
        self,
        mock_log_debug: MagicMock,
        mock_log_error: MagicMock,
        mock_reader: MagicMock,
        mock_file_write: MagicMock,
    ):
        """Tests run_job command when an error writing the file occurs"""
        mock_context = mock_reader.return_value.__enter__.return_value
        mock_context.metadata.return_value = self.example_metadata
        mock_context.description.return_value = self.example_description0
        mock_context.shape.return_value = self.example_shape
        etl_job = BergamoEtl(
            input_source=RESOURCES_DIR,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )
        mock_file_write.side_effect = Exception("An error happened!")

        with self.assertRaises(Exception) as e:
            etl_job.run_job()
        self.assertEqual("An error happened!", str(e.exception))
        mock_file_write.assert_called_once_with(output_directory=RESOURCES_DIR)
        mock_log_error.assert_has_calls(
            [
                call(
                    "Multiple planes not handled in metadata collection."
                    " HANDLE ME!!!: KeyError('userZs')"
                )
            ]
        )
        mock_log_debug.assert_called_once_with(
            "No validation errors detected."
        )

    @patch("logging.warning")
    def test_model_validator(self, mock_log: MagicMock):
        """Tests run_validation_check outputs correctly on invalid model"""
        etl_job = BergamoEtl(
            input_source=RESOURCES_DIR,
            output_directory=RESOURCES_DIR,
            user_settings=self.example_user_settings,
        )

        etl_job._run_validation_check(Session.model_construct())
        mock_log.assert_called_once()


if __name__ == "__main__":
    unittest.main()
