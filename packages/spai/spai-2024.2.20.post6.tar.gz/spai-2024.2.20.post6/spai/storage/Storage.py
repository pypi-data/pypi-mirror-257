import os
from glob import glob
import numpy as np
import pandas as pd
import shutil
import json
import io
from minio import Minio

from .BaseStorage import BaseStorage
from .decorators import with_rio, with_geopandas, with_xarray


class Storage(BaseStorage):
    def __init__(self):
        super().__init__()
        self.storages_names = os.environ.get("SPAI_STORAGE_NAMES", None).split(",")
        self.storages = {}
        self.initialize_storage()

    def __getitem__(self, name):
        return self.storages[name]

    def initialize_storage(self):
        for storage_name in self.storages_names:
            envs = {
                key: value
                for key, value in os.environ.items()
                if key.startswith(f"SPAI_STORAGE_{storage_name.upper()}")
            }
            envs = {key.split("_")[-1].lower(): value for key, value in envs.items()}
            if storage_name.split("_")[0] == "local":
                self.initialize_local(storage_name, envs)
            elif storage_name.split("_")[0] == "s3":
                self.initialize_s3(storage_name, envs)

    def initialize_local(self, name, envs):
        self.storages[f"{name.split('_')[1]}"] = LocalStorage(**envs)

    def initialize_s3(self, name, envs):
        print(envs)
        self.storages[f"{name.split('_')[1]}"] = S3Storage(**envs)


class S3Storage(BaseStorage):
    def __init__(self, url, access, secret, bucket, region=None):
        super().__init__()
        self.url = url
        self.access = access
        self.secret = secret
        self.region = region
        self.bucket = bucket

        if self.access and self.secret:
            # Create a client
            self.client = Minio(
                endpoint=self.url,
                access_key=self.access,
                secret_key=self.secret,
                secure=True if self.region else False,
                region=self.region,
            )  # because no certificate is used in the containerised version of minio
            if not self.client.bucket_exists(self.bucket):
                # Make a bucket with the credentials and the bucket_name given
                self.client.make_bucket(self.bucket)
                print(f"Bucket '{self.bucket}' created")
            else:
                print(f"'{self.bucket}' bucket ready to use")
        else:
            # TODO: create bucket in our minio server (we will need our credentials for that, do it with API request?
            print("Missing credentials")
            # Habría que preguntar si se quiere crear el bucket en nuestro cloud o decirles que introduzcan sus creds

    def list(self, prefix=None):
        if prefix is None:
            return [
                obj.object_name
                for obj in self.client.list_objects(self.bucket, recursive=True)
            ]
        else:
            prefix = prefix.split(".")[-1]
            return [
                obj.object_name
                for obj in self.client.list_objects(
                    self.bucket, prefix=prefix, recursive=True
                )
            ]

    def create_from_path(self, data, name):
        if data.endswith(".json"):
            content_type = "application/json"
            prefix = "json/"
            dst_path = f"{prefix}{name}"
            self.client.fput_object(
                self.bucket, dst_path, data, content_type=content_type
            )
            return dst_path
        elif data.endswith(".tiff") or data.endswith(".tif"):
            content_type = "image/tiff"
            prefix = "tif/"
            dst_path = f"{prefix}{name}"
            # with rasterio.open(data) as src:
            #     self.client.put_object(self.bucket, dst_path, src, length=src.read().all(), content_type=content_type)
            self.client.fput_object(
                self.bucket, dst_path, data, content_type=content_type
            )
            return dst_path
        elif data.endswith(".geojson"):
            content_type = "application/geojson"
            prefix = "geojson/"
            dst_path = f"{prefix}{name}"
            self.client.fput_object(
                self.bucket, dst_path, data, content_type=content_type
            )
            return dst_path
        else:
            print(data)
            # self.client.put_object(self.bucket, prefix + name, data, length, content_type)

    def create_from_dict(self, data, name):
        if name.endswith(".json"):
            content_type = "application/json"
            prefix = "json/"
            dst_path = f"{prefix}{name}"
            content = json.dumps(data, ensure_ascii=False).encode("utf8")
            self.client.put_object(
                self.bucket,
                dst_path,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return dst_path
        elif name.endswith(".geojson"):
            content_type = "application/geojson"
            prefix = "geojson/"
            dst_path = f"{prefix}{name}"
            content = json.dumps(data, ensure_ascii=False).encode("utf8")
            self.client.put_object(
                self.bucket,
                dst_path,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return dst_path
        else:
            raise TypeError("Not a valid dict type extension")

    def create_from_string(self, data, name):
        content_type = "text/plain"
        prefix = "txt/"
        dst_path = f"{prefix}{name}"
        content = data.encode("utf8")
        self.client.put_object(
            self.bucket,
            dst_path,
            io.BytesIO(content),
            -1,
            part_size=50 * 1024 * 1024,
            content_type=content_type,
        )
        return dst_path

    def create_from_dataframe(self, data, name):
        if name.endswith(".csv"):
            content_type = "text/csv"
            prefix = "csv/"
            dst_path = f"{prefix}{name}"
            content = data.to_csv().encode("utf8")
            self.client.put_object(
                self.bucket,
                dst_path,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return dst_path
        elif name.endswith(".json"):
            content_type = "application/json"
            prefix = "json/"
            dst_path = f"{prefix}{name}"
            content = data.to_json().encode("utf8")
            self.client.put_object(
                self.bucket,
                dst_path,
                io.BytesIO(content),
                -1,
                part_size=50 * 1024 * 1024,
                content_type=content_type,
            )
            return dst_path
        else:
            raise TypeError("Not a valid dataframe type extension")

    def read_from_json(self, name):
        try:
            prefix = "json/"
            dst_path = f"{prefix}{name}"
            response = self.client.get_object(self.bucket, dst_path)
            data = json.load(response)
        finally:
            response.close()
            response.release_conn()
        df = pd.DataFrame.from_dict(data)
        # Convert the index to integers (the timestamps) and then to datetime
        df.index = pd.to_datetime(df.index.astype(int), unit="ms")
        # Now your index is a datetime object and you can use strftime
        df.index = df.index.strftime("%Y-%m-%d")
        return df

    @with_geopandas
    def read_from_geojson(self, gpd, name):
        try:
            prefix = "geojson/"
            dst_path = f"{prefix}{name}"
            response = self.client.get_object(self.bucket, dst_path)
            data = json.load(response)
        finally:
            response.close()
            response.release_conn()
        return gpd.GeoDataFrame.from_features(data)

    @with_rio
    def read_from_rasterio(self, rio, name):
        try:
            prefix = "tif/"
            dst_path = f"{prefix}{name}"
            response = self.client.get_object(self.bucket, dst_path)
            data = response
        finally:
            response.close()
            response.release_conn()
        return rio.open(data)


class LocalStorage(BaseStorage):
    def __init__(self, path="data"):
        super().__init__()
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print(f"'{self.path}' created")
        else:
            print(f"'{self.path}' folder ready to use")

    def exists(self, name):
        return os.path.exists(self.get_path(name))

    def get_path(self, name):
        return os.path.join(self.path, name)

    def create_from_path(self, data, name):
        dst_path = self.get_path(name)
        shutil.move(data, dst_path)  # porque se hace un move en vez de un copy?
        return dst_path

    def create_from_dict(self, data, name):
        if name.endswith(".json") or name.endswith(".geojson"):
            dst_path = self.get_path(name)
            with open(dst_path, "w") as f:
                json.dump(data, f)
            return dst_path
        else:
            raise TypeError("Not a valid dict type extension")

    def create_from_string(self, data, name):
        dst_path = self.get_path(name)
        with open(dst_path, "w") as f:
            f.write(data)
        return dst_path

    def create_from_dataframe(self, data, name):
        if name.endswith(".csv"):
            dst_path = self.get_path(name)
            data.to_csv(dst_path)
            return dst_path
        elif name.endswith(".json"):
            dst_path = self.get_path(name)
            data.to_json(dst_path)
            return dst_path

    def create_from_image(self, data, name):
        dst_path = self.get_path(name)
        data.save(dst_path)
        return dst_path

    @with_rio
    def create_from_rasterio(self, rio, x, name, ds, window=None):
        dst_path = self.get_path(name)
        kwargs = ds.meta.copy()
        transform = ds.transform if window is None else ds.window_transform(window)
        kwargs.update(
            driver="GTiff",
            count=1 if x.ndim < 3 else x.shape[0],
            height=x.shape[0] if x.ndim < 3 else x.shape[1],
            width=x.shape[1] if x.ndim < 3 else x.shape[2],
            dtype=np.uint8 if x.dtype == "bool" else x.dtype,
            crs=ds.crs,
            transform=transform,
            # nbits=1 if x.dtype == 'bool' else
        )
        with rio.open(dst_path, "w", **kwargs) as dst:
            bands = 1 if x.ndim < 3 else [i + 1 for i in range(x.shape[0])]
            dst.write(x, bands)
        return dst_path

    def create_from_array(self, data, name):
        dst_path = self.get_path(name)
        np.save(dst_path, data)
        return dst_path

    def create_from_csv(self, data, name):
        dst_path = self.get_path(name)
        data.to_csv(dst_path)
        return dst_path

    def create_from_json(self, data, name):
        dst_path = self.get_path(name)
        data.to_json(dst_path)
        return dst_path

    def create_from_parquet(self, data, name):
        dst_path = self.get_path(name)
        data.to_parquet(dst_path)
        return dst_path

    def create_from_zarr(self, data, name):
        dst_path = self.get_path(name)
        data.to_zarr(dst_path)
        return dst_path

    def list(self, pattern="*"):
        paths = glob(os.path.join(self.path, pattern))
        # strip base path
        return [p.replace(self.path + "/", "") for p in paths]

    def read_from_array(self, name, path=None):
        if path is None:
            path = self.get_path(name)
        return np.load(path)

    @with_rio
    def read_from_rasterio(self, rio, name):
        return rio.open(self.get_path(name))

    def read_from_csv(self, name):
        return pd.read_csv(self.get_path(name), index_col=0)

    def read_from_json(self, name):
        return pd.read_json(self.get_path(name))

    @with_geopandas
    def read_from_geojson(self, gpd, name):
        return gpd.read_file(self.get_path(name))

    @with_geopandas
    def read_from_parquet(self, gpd, name):
        return gpd.read_parquet(self.get_path(name))

    @with_xarray
    def read_from_zarr(self, xr, name):
        return xr.open_zarr(self.get_path(name))
