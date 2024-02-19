from typing import List, Union, Dict

from pydantic import BaseModel


class TaxPredictParam(BaseModel):
    """
    税收分类识别服务 参数模型
    """
    # 序列化
    sn: str = None
    # 输入文本
    text: str = None


class OssZipDirParam(BaseModel):
    """
    OSS目录压缩
    """
    # 桶名称
    bucket_name: str = None
    # 待压缩对象前缀
    object_prefix: str = None
    # 最终输出对象名
    dist_object_name: str = None


class BucketObject(BaseModel):
    """
    OSS文件压缩，中间对象
    """
    # 桶名
    bucket_name: str = None
    # 源对象名称
    src_object_key: str = None
    # 输出对象名称
    output_object_key: str = None


class OssZipFilesParam(BaseModel):
    """
    OSS目录压缩
    """
    # 待压缩对象列表
    src_object_list: List[BucketObject]
    # 最终输出桶名称
    dist_bucket_name: str = None
    # 最终输出对象名
    dist_object_name: str = None


class SkuSearchParam(BaseModel):
    """
    搜索同款商品参数
    """
    # 页码
    page: int = 1
    # 搜索关键字
    text: str = None
