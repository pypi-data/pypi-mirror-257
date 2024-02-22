# GeoServer Config

Configuration for geoserver and additional resources needed to host stuff there.

## Docker in EC2

### EC2 Setup

Launch an instance using [this user data](config/ec2/user_data.sh). It is recommended the instance to have >=8Gb RAM and >=30Gb ephemeral storage. A good alternative is the `t3.large` which costs ~60 USD/month as of 02/10/2023.

Connect to your instance and add docker to user group by running:

```bash
sudo usermod -aG docker $USER
newgrp docker # restarts docker
```

### Launch Geoserver

Pull the geoserver image:

```bash
docker pull docker.osgeo.org/geoserver:2.23.x 
```

Now run the container, installing COG extension and using a local data directory at `/MY/DATADIRECTORY`. As detailed in the documentation: *this setup allows direct management of the file data shared with the container. This setup is also easy to update to use the latest container.*

```bash
docker run --mount type=bind,src=/MY/DATADIRECTORY,target=/opt/geoserver_data -it -p8080:8080 --env INSTALL_EXTENSIONS=true --env COMMUNITY_EXTENSIONS="cog" --env JAVA_TOOL_OPTIONS="-Xmx4096m" docker.osgeo.org/geoserver:2.23.x
```

**The `JAVA_TOOL_OPTIONS` is important to increase the maximum hava heap size available for the app**. The example command provided earlier sets this limit on ~4Gb For coverage stores, a large heap size is necessary since there is a lot of data to bring. You can adjust it according to your use case. Run `java -XX:+PrintFlagsFinal -version | grep MaxHeapSize` for getting the max heat space in the docker container.


### Optimization of Geoserver ImageMosaic

- [See geoserver documentation](https://training.geonode.geosolutionsgroup.com/master/GN2/ADV_LAYERS_PUB/OPTIMIZE_RASTER.html)

## Example Notebooks

- **Coverage Store using Cog Images**: setup a WMS/WMTS-T service using COG rasters located in cloud storage

## TODO

- [ ] Fix creating new datastore with existing database index: [geoserver repo issue](https://osgeo-org.atlassian.net/jira/software/c/projects/GEOS/issues/GEOS-11144)