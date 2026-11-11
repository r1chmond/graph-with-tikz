from typing import Any, TypedDict
from app.constants import GLOBAL_PROP_KEYWORDS, TOP_LEVEL_KEYWORDS, VERTEX_PROP_KEYWORDS
from app.data import ValidationError


class VertexChecker(TypedDict):
    label: str
    type: str
    next: list
    fontColor: str
    shapeColor: str
    shapeFill: str


def validate_data(data: object) -> dict[str, Any]:
    result = {}
    check_top_level(data)

    # ensure top level keys are of the same type
    # and its values are dict

    # check that value keys(properties) are valid
    for vid, props in data.items():
        new_val = {}

        if vid not in TOP_LEVEL_KEYWORDS and vid not in GLOBAL_PROP_KEYWORDS:
            for prop, prop_val in props.items():
                if not (prop in VERTEX_PROP_vidWORDS or prop in GLOBAL_PROP_KEYWORDS):
                    raise ValidationError(f"Unrecognised property {prop!r}")
                # check 'next' prop's value is a list
                if prop == "next" and isinstance(prop_val, list):
                    new_next_list = []
                    # remove duplicates and ensure element are of the
                    # same type
                    seen: set[str] = set()
                    for idx in prop_val:
                        if idx not in seen:
                            if isinstance(idx, (int, float)):
                                new_next_list.append(str(idx))
                            elif isinstance(idx, str):
                                new_next_list.append(idx)
                            else:
                                raise ValidationError(
                                    f"Expect a list but got {type(idx).__name__}"
                                )
                        seen.add(idx)

                    new_val["next"] = new_next_list

                elif prop != "next":
                    new_val[prop] = prop_val
                else:
                    raise ValidationError(
                        f"Expect a list but got {type(prop_val).__name__}"
                    )

            result[str(vid)] = new_val

    return result


def check_top_level(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValidationError(
            f"Expected a dict at the top level but got {type(data).__name__}"
        )


def validate_vertex(props: dict) -> dict[str, Any]:
    validated_props = {}
    for prop, prop_val in props:
        if not (prop in VERTEX_PROP_KEYWORDS or prop in GLOBAL_PROP_KEYWORDS):
            raise ValidationError(f"Unrecognised property {prop!r}")
        # check 'next' prop's value is a list
        if prop == "next" and isinstance(prop_val, list):
            new_next_list = normalise_next("", prop_val)
            validated_props["next"] = new_next_list

        elif prop != "next":
            validated_props[prop] = prop_val
        else:
            raise ValidationError(f"Expect a list but got {type(prop_val).__name__}")

    return validated_props


def normalise_next(vid: str, values: list[Any]) -> list[str]:
    new_next_list: list[str] = []
    seen: set[str] = set()
    for idx in values:
        normalised = normalise_id(idx)
        if normalised not in seen:
            new_next_list.append(normalised)
            seen.add(normalised)

    return new_next_list


def normalise_id(value: Any) -> str:
    if isinstance(value, (int | float)):
        return str(value)

    elif isinstance(value, str):
        return value
    else:
        raise ValidationError(f"Expected str but got {type(value).__name__}")
