import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.create_pet_input import CreatePetInput  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server.models.pet_page import PetPage  # noqa: E501
from openapi_server.models.pet_status import PetStatus  # noqa: E501
from openapi_server.models.update_pet_input import UpdatePetInput  # noqa: E501
from openapi_server import util


def create_pets(body):  # noqa: E501
    """Thêm thú cưng mới

    Chỉ name là bắt buộc; status mặc định available. # noqa: E501

    :param create_pet_input: 
    :type create_pet_input: dict | bytes

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    create_pet_input = body
    if flask.request.is_json:
        create_pet_input = CreatePetInput.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_pet(pet_id):  # noqa: E501
    """Xoá thú cưng

    Xoá vĩnh viễn; thành công trả 204 không có body. # noqa: E501

    :param pet_id: ID của thú cưng
    :type pet_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_pets(limit=None, offset=None, status=None):  # noqa: E501
    """Liệt kê thú cưng

    Phân trang offset (0-based), tối đa 100 item/trang, sort theo id tăng dần. # noqa: E501

    :param limit: Số item mỗi trang (1-100)
    :type limit: int
    :param offset: Số item bỏ qua (0-based)
    :type offset: int
    :param status: Lọc theo trạng thái; bỏ trống &#x3D; tất cả
    :type status: dict | bytes

    :rtype: Union[PetPage, Tuple[PetPage, int], Tuple[PetPage, int, Dict[str, str]]
    """
    if flask.request.is_json:
        status =  PetStatus.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def show_pet_by_id(pet_id):  # noqa: E501
    """Xem chi tiết thú cưng

    Trả đầy đủ thông tin thú cưng; 404 nếu không tồn tại. # noqa: E501

    :param pet_id: ID của thú cưng
    :type pet_id: int

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    return 'do some magic!'


def update_pet(pet_id, body):  # noqa: E501
    """Cập nhật một phần thú cưng

    Chỉ gửi trường cần đổi (tối thiểu 1); gửi null cho tag để xoá giá trị. # noqa: E501

    :param pet_id: ID của thú cưng
    :type pet_id: int
    :param update_pet_input: 
    :type update_pet_input: dict | bytes

    :rtype: Union[Pet, Tuple[Pet, int], Tuple[Pet, int, Dict[str, str]]
    """
    update_pet_input = body
    if flask.request.is_json:
        update_pet_input = UpdatePetInput.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'
