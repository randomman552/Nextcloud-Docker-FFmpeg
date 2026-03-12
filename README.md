# Nextcloud With FFmpeg
The Docker images created by nextcloud do not include FFmpeg which is required for video previews and some nextcloud apps.

The image hosted with this repository extends the nextcloud images with an ffmpeg installation.

## Using this image
To use this image, simply use the `ghcr.io/randomman552/nextcloud-docker-ffmpeg` instead of `nextcloud`.

For example, view the below `compose.yml` adapted from the [nextcloud image on Docker Hub](https://hub.docker.com/_/nextcloud/):

```yaml
version: '3'

volumes:
  nextcloud:
  db:

services:
  db:
    image: mariadb:10.5
    restart: always
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
    volumes:
      - db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=
      - MYSQL_PASSWORD=
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  app:
    image: ghcr.io/randomman552/nextcloud-docker-ffmpeg
    restart: always
    ports:
      - 8080:80
    links:
      - db
    volumes:
      - nextcloud:/var/www/html
    environment:
      - MYSQL_PASSWORD=
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_HOST=db
```
