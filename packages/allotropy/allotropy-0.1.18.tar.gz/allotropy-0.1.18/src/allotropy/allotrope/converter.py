from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, Callable, cast, get_args, get_origin, Optional, Union

from allotropy.allotrope.models.shared.definitions.definitions import (
    InvalidJsonFloat,
    TDimensionArray,
    TFunction,
    TMeasureArray,
)
from cattrs import Converter
from cattrs.errors import ClassValidationError
from cattrs.gen import make_dict_structure_fn, override

# TODO(brian): sort
SPECIAL_KEYS = {  # TODO sync with allotropy
    "manifest": "$asm.manifest",
    "cube_structure": "cube-structure",
    "field_componentDatatype": "@componentDatatype",
    "field_asm_fill_value": "$asm.fill-value",
    "field_type": "@type",
    "field_index": "@index",
    "scan_position_setting__plate_reader_": "scan position setting (plate reader)",
    "detector_distance_setting__plate_reader_": "detector distance setting (plate reader)",
    "cell_type__cell_counter_": "cell type (cell counter)",
    "dead_cell_density__cell_counter_": "dead cell density (cell counter)",
    "average_dead_cell_diameter__cell_counter_": "average dead cell diameter (cell counter)",
    "viability__cell_counter_": "viability (cell counter)",
    "total_cell_density__cell_counter_": "total cell density (cell counter)",
    "viable_cell_density__cell_counter_": "viable cell density (cell counter)",
    "average_live_cell_diameter__cell_counter_": "average live cell diameter (cell counter)",
    "average_total_cell_diameter__cell_counter_": "average total cell diameter (cell counter)",
    "total_cell_diameter_distribution__cell_counter_": "total cell diameter distribution (cell counter)",
    "viable_cell_count__cell_counter_": "viable cell count (cell counter)",
    "total_cell_count__cell_counter_": "total cell count (cell counter)",
    "autosampler_injection_volume_setting__chromatography_": "autosampler injection volume setting (chromatography)",
    "capacity_factor__chromatography_": "capacity factor (chromatography)",
    "peak_selectivity__chromatography_": "peak selectivity (chromatography)",
    "peak_width_at_4_4___of_height": "peak width at 4.4 % of height",
    "peak_width_at_13_4___of_height": "peak width at 13.4 % of height",
    "peak_width_at_32_4___of_height": "peak width at 32.4 % of height",
    "peak_width_at_60_7___of_height": "peak width at 60.7 % of height",
    "peak_width_at_5___of_height": "peak width at 5 % of height",
    "peak_width_at_10___of_height": "peak width at 10 % of height",
    "statistical_skew__chromatography_": "statistical skew (chromatography)",
    "asymmetry_factor_measured_at_5___height": "asymmetry factor measured at 5 % height",
    "asymmetry_factor_measured_at_10___height": "asymmetry factor measured at 10 % height",
    "asymmetry_factor_squared_measured_at_10___height": "asymmetry factor squared measured at 10 % height",
    "asymmetry_factor_squared_measured_at_4_4___height": "asymmetry factor squared measured at 4.4 % height",
    "asymmetry_factor_measured_at_4_4___height": "asymmetry factor measured at 4.4 % height",
    "number_of_theoretical_plates__chromatography_": "number of theoretical plates (chromatography)",
    "number_of_theoretical_plates_measured_at_60_7___of_peak_height": "number of theoretical plates measured at 60.7 % of peak height",
    "number_of_theoretical_plates_measured_at_32_4___of_peak_height": "number of theoretical plates measured at 32.4 % of peak height",
    "number_of_theoretical_plates_measured_at_13_4___of_peak_height": "number of theoretical plates measured at 13.4 % of peak height",
    "number_of_theoretical_plates_measured_at_4_4___of_peak_height": "number of theoretical plates measured at 4.4 % of peak height",
    "number_of_theoretical_plates_by_peak_width_at_half_height__JP14_": "number of theoretical plates by peak width at half height (JP14)",
    "co2_saturation": "CO2 saturation",
    "o2_saturation": "O2 saturation",
    "pco2": "pCO2",
    "po2": "pO2",
}
SPECIAL_KEYS_INVERSE: dict[str, str] = dict(
    cast(tuple[str, str], reversed(item)) for item in SPECIAL_KEYS.items()
)


def register_data_cube_hooks(converter: Converter) -> None:
    converter.register_structure_hook(
        Union[TDimensionArray, TFunction],
        lambda val, _: val if isinstance(val, list) else converter.structure(val, TFunction),
    )
    converter.register_structure_hook(TMeasureArray, lambda val, _: val)


def register_str_union_hooks(converter: Converter) -> None:
    def is_str_union(val: Any) -> bool:
        if get_origin(val) != Union:
            return False
        args = set(get_args(val))
        if str not in args:
            return False
        args.remove(str)
        args.discard(type(None))
        if len(args) != 1:
            return False
        return is_dataclass(args.pop())

    def str_union_structure_fn(
        cls: Any,
    ) -> Callable[[Optional[Union[dict, str]], Any], Optional[Union[str, Any]]]:
        def structure_item(val: Optional[Union[dict, str]], _: Any) -> Optional[Union[str, cls]]:
            if val is None:
                return None
            if type(val) == str:
                return val
            return converter.structure(val, cls)

        return structure_item

    converter.register_structure_hook_factory(is_str_union, str_union_structure_fn)


def register_bool_union_hooks(converter: Converter) -> None:
    def is_bool_union(val: Any) -> bool:
        if get_origin(val) != Union:
            return False
        args = set(get_args(val))
        if bool not in args:
            return False
        args.remove(bool)
        args.discard(type(None))
        if len(args) != 1:
            return False
        return is_dataclass(args.pop())

    def bool_union_structure_fn(
        cls: Any,
    ) -> Callable[[Optional[Union[dict, bool]], Any], Optional[Union[bool, Any]]]:
        def structure_item(val: Optional[Union[dict, bool]], _: Any) -> Optional[Union[bool, cls]]:
            if val is None:
                return None
            if type(val) == bool:
                return val
            return converter.structure(val, cls)

        return structure_item

    converter.register_structure_hook_factory(is_bool_union, bool_union_structure_fn)


def register_float_invalid_union_hooks(converter: Converter) -> None:
    def is_float_invalid_union(val: Any) -> bool:
        if get_origin(val) != Union:
            return False
        return set(get_args(val)) == {float, InvalidJsonFloat}

    def float_invalid_union_structure_fn(
        _: Any,
    ) -> Callable[[Optional[Union[float, InvalidJsonFloat]], Any], Optional[Union[float, str]]]:
        def structure_item(val: Union[float, InvalidJsonFloat], _: Any) -> Union[float, str]:
            return val

        return structure_item

    converter.register_structure_hook_factory(is_float_invalid_union, float_invalid_union_structure_fn)


def register_dict_hooks(converter: Converter) -> None:
    def dict_structure_fn(cls: Any) -> Callable[[Any, Any], dict]:
        return make_dict_structure_fn(
            cls,
            converter,
            **{
                a.name: override(rename=SPECIAL_KEYS.get(a.name, a.name.replace("_", " ")))
                for a in fields(cls)
            },
        )

    converter.register_structure_hook_factory(is_dataclass, dict_structure_fn)


def register_dataclass_union_hooks(converter: Converter) -> None:
    def is_dataclass_union(val: Any) -> bool:
        if get_origin(val) != Union:
            return False
        args = set(get_args(val))
        args.discard(type(None))
        return len(args) > 1 and all(is_dataclass(arg) for arg in args)

    def dataclass_union_structure_fn(
        cls: Any,
    ) -> Callable[[Optional[dict], Any], Optional[Any]]:
        def structure_item(val: Optional[dict], _: Any) -> Optional[cls]:
            for subcls in get_args(cls):
                try:
                    return converter.structure(val, subcls)
                except ClassValidationError:
                    pass

            exc = f"Failed to parse dict into any valid class of {cls}"
            raise ClassValidationError(exc)

        return structure_item

    converter.register_structure_hook_factory(is_dataclass_union, dataclass_union_structure_fn)


def setup_converter(register_additional_hooks_fn: Optional[Callable[[Converter], None]] = None) -> Converter:
    converter = Converter()
    register_data_cube_hooks(converter)
    if register_additional_hooks_fn is not None:
        register_additional_hooks_fn(converter)
    register_str_union_hooks(converter)
    register_bool_union_hooks(converter)
    register_dict_hooks(converter)
    register_dataclass_union_hooks(converter)
    register_float_invalid_union_hooks(converter)
    return converter
