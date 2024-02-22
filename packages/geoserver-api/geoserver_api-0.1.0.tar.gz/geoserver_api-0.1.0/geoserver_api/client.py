import os
import urllib
from pprint import pprint

import requests


class GeoServerClient:
    workspace = None

    def __init__(self, server_url: str, username: str, password: str):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.url = os.path.join(os.environ["GEOSERVER_URL"], "geoserver/rest")

    def reload_config(self):
        """
        Reloads the GeoServer catalog and configuration from disk.
        This operation is used in cases where an external tool has modified the on-disk configuration.
        This operation will also force GeoServer to drop any internal caches and reconnect to all data stores.
        """
        try:
            self.session.post(url=f"{self.url}/reload")
            print("Geoserver config reloaded")
        except Exception as e:
            print(f"Error reloading config: {e}")

    def __coveragestore_url(
        self,
    ) -> str:
        return os.path.join(self.url, f"workspaces/{self.workspace}/coveragestores")

    def set_workspace(self, workspace: str):
        self.workspace = workspace

    def create_empty_mosaic(self, coverage_store: str, zip_path: str):
        """Creates an empty mosaic in geoserver

        Args:
            coverage_name (str): name of the coverage store
            zip_path (str): path to a .zip file containing .properties configuration files
            for mosaic
        """
        with open(zip_path, "rb") as zip:
            data = zip.read()
        response = self.session.put(
            url=os.path.join(
                self.__coveragestore_url(),
                f"{coverage_store}/file.imagemosaic?configure=none",
            ),
            data=data,
            headers={"Content-Type": "application/zip"},
        )
        pprint(response.status_code)

    def setup_mosaic_config(self, coverage_store: str, xml_path: str):
        """Sends an xml with the mosaic configuration to the geoserver

        Args:
            coverage_store (str): name of the coveragestore to configure
            xml_path (str): path to xml
        """
        # open xml file and send it to geoserver
        with open(xml_path) as xml:
            response = self.session.post(
                url=os.path.join(
                    self.__coveragestore_url(),
                    f"{coverage_store}/coverages",
                ),
                data=xml,
                headers={"Content-Type": "text/xml"},
            )
            pprint(response.status_code)

    def delete_mosaic_granule(
        self, coverage_store: str, coverage_name: str, granule_id: str
    ):
        """deletes granule based on it's id

        Args:
            coverage_store (str): name of coverage store that contains granule
            coverage_name (str): name of the coverage layer
            granule_id (str): granule identifier. Accessible through the index of granules.
        """
        try:
            response = self.session.delete(
                url=os.path.join(
                    self.__coveragestore_url(),
                    f"{coverage_store}/coverages/{coverage_name}/index/granules/{granule_id}",
                )
            )
            pprint(response.status_code)
        except Exception as e:
            print(f"Error deleting granule: {e}")
        pass

    def add_mosaic_granule(self, coverage_store: str, granule_path: str):
        """Adds a new granule to an existing imagemosaic

        Args:
            coverage_store (str): name of the coverage store
            granule_path (str): url to granule
        """
        response = self.session.post(
            url=os.path.join(
                self.__coveragestore_url(), f"{coverage_store}/remote.imagemosaic"
            ),
            data=granule_path,
            headers={"Content-Type": "text/plain"},
        )
        response.raise_for_status()
        return response

    def list_coverages(self, coverage_store: str):
        """Lists all coverages currently hosted in specified coverage store"""
        response = self.session.get(
            url=os.path.join(
                self.__coveragestore_url(), f"{coverage_store}/coverages.xml?list=all"
            )
        )
        pprint(response.text)

    def list_mosaic_granules(
        self, coverage_store: str, coverage: str, filter: str = ""
    ):
        """Lists all granules belonging to a specified coverage"""
        query_url = f"{coverage_store}/coverages/{coverage}/index/granules.json"
        if filter != "":
            filter = urllib.parse.quote(filter)
            query_url += f"?filter={filter}"
        response = self.session.get(
            url=os.path.join(
                self.__coveragestore_url(),
                query_url,
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed listing mosaic granules: {response}")

    def delete_coverage_store(self, coverage_store: str):
        """Warning: this doesn't delete the folder of the coverage in the geoserver/data/<workspace>/ directory. If you want
        to create another coveragestore with this name, you should also erase it.

        IMPORTANT: this method doesn't delete the Postgres DATABASE, if created. Consider manually deleting it if necessary

        Args:
            coverage_store (str): name of the coverage store to delete
        """
        response = self.session.delete(
            url=os.path.join(
                self.__coveragestore_url(), f"{coverage_store}?recurse=true"
            )
        )
        pprint(response.status_code)
