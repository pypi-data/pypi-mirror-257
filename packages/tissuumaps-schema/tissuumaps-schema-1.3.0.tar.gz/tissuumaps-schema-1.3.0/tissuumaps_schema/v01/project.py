import json
from enum import Enum
from typing import Any, ClassVar, Optional, Type, Union

from pydantic import ConfigDict, Field

from ..base import RootSchemaBaseModel, SchemaBaseModel
from ..v00 import Project as ProjectV00
from .base import RootSchemaBaseModelV01


class ColorScale(str, Enum):
    INTERPOLATE_CUBEHELIX_DEFAULT = "interpolateCubehelixDefault"
    INTERPOLATE_RAINBOW = "interpolateRainbow"
    INTERPOLATE_WARM = "interpolateWarm"
    INTERPOLATE_COOL = "interpolateCool"
    INTERPOLATE_VIRIDIS = "interpolateViridis"
    INTERPOLATE_MAGMA = "interpolateMagma"
    INTERPOLATE_INFERNO = "interpolateInferno"
    INTERPOLATE_PLASMA = "interpolatePlasma"
    INTERPOLATE_BLUES = "interpolateBlues"
    INTERPOLATE_BR_BG = "interpolateBrBG"
    INTERPOLATE_BU_GN = "interpolateBuGn"
    INTERPOLATE_BU_PU = "interpolateBuPu"
    INTERPOLATE_CIVIDIS = "interpolateCividis"
    INTERPOLATE_GN_BU = "interpolateGnBu"
    INTERPOLATE_GREENS = "interpolateGreens"
    INTERPOLATE_GREYS = "interpolateGreys"
    INTERPOLATE_OR_RD = "interpolateOrRd"
    INTERPOLATE_ORANGES = "interpolateOranges"
    INTERPOLATE_PR_GN = "interpolatePRGn"
    INTERPOLATE_PI_YG = "interpolatePiYG"
    INTERPOLATE_PU_BU = "interpolatePuBu"
    INTERPOLATE_PU_BU_GN = "interpolatePuBuGn"
    INTERPOLATE_PU_OR = "interpolatePuOr"
    INTERPOLATE_PU_RD = "interpolatePuRd"
    INTERPOLATE_PURPLES = "interpolatePurples"
    INTERPOLATE_RD_BU = "interpolateRdBu"
    INTERPOLATE_RD_GY = "interpolateRdGy"
    INTERPOLATE_RD_PU = "interpolateRdPu"
    INTERPOLATE_RD_YL_BU = "interpolateRdYlBu"
    INTERPOLATE_RD_YL_GN = "interpolateRdYlGn"
    INTERPOLATE_REDS = "interpolateReds"
    INTERPOLATE_SINEBOW = "interpolateSinebow"
    INTERPOLATE_SPECTRAL = "interpolateSpectral"
    INTERPOLATE_TURBO = "interpolateTurbo"
    INTERPOLATE_YL_GN = "interpolateYlGn"
    INTERPOLATE_YL_GN_BU = "interpolateYlGnBu"
    INTERPOLATE_YL_OR_BR = "interpolateYlOrBr"
    INTERPOLATE_YL_OR_RD = "interpolateYlOrRd"


class CompositeMode(str, Enum):
    SOURCE_OVER = "source-over"
    LIGHTER = "lighter"
    DARKEN = "darken"
    SOURCE_ATOP = "source-atop"
    SOURCE_IN = "source-in"
    SOURCE_OUT = "source-out"
    DESTINATION_OVER = "destination-over"
    DESTINATION_ATOP = "destination-atop"
    DESTINATION_IN = "destination-in"
    DESTINATION_OUT = "destination-out"
    COPY = "copy"
    XOR = "xor"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    COLOR_DODGE = "color-dodge"
    COLOR_BURN = "color-burn"
    HARD_LIGHT = "hard-light"
    SOFT_LIGHT = "soft-light"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"


class Filter(str, Enum):
    COLOR = "Color"
    BRIGHTNESS = "Brightness"
    EXPOSURE = "Exposure"
    HUE = "Hue"
    CONTRAST = "Contrast"
    VIBRANCE = "Vibrance"
    NOISE = "Noise"
    SATURATION = "Saturation"
    GAMMA = "Gamma"
    INVERT = "Invert"
    GREYSCALE = "Greyscale"
    THRESHOLD = "Threshold"
    EROSION = "Erosion"
    DILATION = "Dilation"
    SPLIT_CHANNEL = "SplitChannel"
    COLORMAP = "Colormap"


class Shape(str, Enum):
    CROSS = "cross"
    DIAMOND = "diamond"
    SQUARE = "square"
    TRIANGLE_UP = "triangle up"
    STAR = "star"
    CLOBBER = "clobber"
    DISC = "disc"
    HBAR = "hbar"
    VBAR = "vbar"
    TAILED_ARROW = "tailed arrow"
    TRIANGLE_DOWN = "triangle down"
    RING = "ring"
    X = "x"
    ARROW = "arrow"


class LayoutAxis(str, Enum):
    HORIZONTALLY = "horizontally"
    VERTICALLY = "vertically"


class CollectionLayout(SchemaBaseModel):
    immediately: Optional[bool] = Field(
        default=False,
        description="Whether to animate to the new arrangement.",
    )
    layout: Optional[LayoutAxis] = Field(
        default=None,
        description="See collectionLayout in OpenSeadragon.Options.",
    )
    rows: Optional[int] = Field(
        default=None,
        description="See collectionRows in OpenSeadragon.Options.",
    )
    columns: Optional[int] = Field(
        default=None,
        description="See collectionColumns in OpenSeadragon.Options.",
    )
    tileSize: Optional[float] = Field(
        default=None,
        description="See collectionTileSize in OpenSeadragon.Options.",
    )
    tileMargin: Optional[float] = Field(
        default=None,
        description="See collectionTileMargin in OpenSeadragon.Options.",
    )


class LayerClip(SchemaBaseModel):
    x: float = Field(
        description="Left coordinate of the clip in image pixel coordinate."
    )
    y: float = Field(
        description="Top coordinate of the clip in image pixel coordinate."
    )
    w: float = Field(description="Width of the clip in image pixel coordinate.")
    h: float = Field(description="Height of the clip in image pixel coordinate.")


class Layer(SchemaBaseModel):
    name: str = Field(description="Name of the image layer")
    tile_source: str = Field(
        alias="tileSource",
        description="Relative path to an image file in a supported format.",
    )
    x: Optional[float] = Field(
        default=None, description="Left coordinate of the image in viewport coordinate."
    )
    y: Optional[float] = Field(
        default=None, description="Top coordinate of the image in viewport coordinate."
    )
    rotation: Optional[float] = Field(
        default=None, description="Rotation of the image in degrees."
    )
    flip: bool = Field(
        default=False,
        description="Flip the image horizontally.",
    )
    scale: Optional[float] = Field(default=None, description="Scale of the image.")
    clip: Optional[LayerClip] = Field(
        default=None,
        description=(
            "Bounding box used to clip image in image pixel coordinate. If not "
            "specified, the whole image is shown."
        ),
    )


class LayerFilter(SchemaBaseModel):
    name: Filter = Field(description="Filter name.")
    value: Union[str, bool, int, float] = Field(description="Filter parameter.")


class BoundingBox(SchemaBaseModel):
    x: float = Field(
        description="Left coordinate of the bounding box in viewport coordinate."
    )
    y: float = Field(
        description="Top coordinate of the bounding box in viewport coordinate."
    )
    width: float = Field(
        description="Width of the bounding box in viewport coordinate."
    )
    height: float = Field(
        description="Height of the bounding box in viewport coordinate."
    )


class Setting(SchemaBaseModel):
    module: str = Field(description="Module where the function or property lies.")
    function: str = Field(description="Function or property of the given module.")
    value: Any


class ExpectedHeader(SchemaBaseModel):
    x: str = Field(alias="X", description="Name of CSV column to use as X-coordinate.")
    y: str = Field(alias="Y", description="Name of CSV column to use as Y-coordinate.")
    gb_col: Optional[str] = Field(
        default=None,
        description="Name of CSV column to use as key to group markers by.",
    )
    gb_name: Optional[str] = Field(
        default=None,
        description="Name of CSV column to display for groups instead of group key.",
    )
    cb_cmap: Optional[str] = Field(
        default=None,
        description="Name of D3 color scale to be used for color mapping.",
    )
    cb_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing scalar values for color mapping or "
            "hexadecimal RGB colors in format '#ff0000'."
        ),
    )
    cb_gr_dict: Union[str, dict[str, Any], list[str]] = Field(
        default="",
        description=(
            "JSON string specifying a custom dictionary for mapping group keys to "
            "group colors. Example: "
            "``\"{'key1': '#ff0000', 'key2': '#00ff00', 'key3': '#0000ff'}\"``."
        ),
    )
    scale_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing scalar values for changing the size of "
            "markers."
        ),
    )
    scale_factor: float = Field(
        default=1.0,
        description=(
            "Numerical value for a fixed scale factor to be applied to markers."
        ),
    )
    coord_factor: float = Field(
        default=1.0,
        description=(
            "Numerical value for a fixed scale factor to be applied to marker "
            "coordinates."
        ),
    )
    pie_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing data for pie chart sectors. TissUUmaps "
            "expects labels and numerical values for sectors to be separated by ':' "
            "characters in the CSV column data."
        ),
    )
    pie_dict: Union[str, dict[str, Any], list[str]] = Field(
        default="",
        description=(
            "JSON string specifying a custom dictionary for mapping pie chart sector "
            "indices to colors. Example: "
            "``\"{0: '#ff0000', 1: '#00ff00', 2: '#0000ff'}\"``. If no dictionary is "
            "specified, TissUUmaps will use a default color palette instead."
        ),
    )
    shape_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing a name or an index for marker shape."
        ),
    )
    shape_fixed: str = Field(
        default="cross",
        description="Name or index of a single fixed shape to be used for all markers.",
    )
    shape_gr_dict: Union[str, dict[str, Any], list[str]] = Field(
        default="",
        description=(
            "JSON string specifying a custom dictionary for mapping group keys to "
            "group shapes. Example: "
            "``\"{'key1': 'square', 'key2': 'diamond', 'key3': 'triangle up'}\"``."
        ),
    )
    edges_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing a name or an index for marker edges "
            "in Network Diagram mode."
        ),
    )
    collectionItem_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing a name or an index for marker collection "
            "items in Collection mode."
        ),
    )
    collectionItem_fixed: Union[str, int] = Field(
        default=0,
        description=(
            "Name or index of a single fixed collection item to be used for all "
            "markers in Collection mode."
        ),
    )
    opacity_col: Optional[str] = Field(
        default=None,
        description="Name of CSV column containing scalar values for opacities.",
    )
    opacity: float = Field(
        default=1.0,
        description=(
            "Numerical value for a fixed opacity factor to be applied to markers."
        ),
    )
    stroke_width: float = Field(
        default=2.5,
        description="Numerical value for the marker stroke width.",
    )
    sortby_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing scalar values for sorting markers."
        ),
    )
    z_order: float = Field(
        default=1.0,
        description="Numerical value of z-order to be used for all markers.",
    )
    tooltip_fmt: str = Field(
        default="",
        description=(
            "Custom formatting string used for displaying metadata about a selected "
            "marker. See https://github.com/TissUUmaps/TissUUmaps/issues/2 for an "
            "overview of the grammer and keywords. If no string is specified, "
            "TissUUmaps will show default metadata depending on the context."
        ),
    )


class ExpectedRadios(SchemaBaseModel):
    cb_col: bool = Field(
        default=False,
        description="If markers should be colored by data in CSV column.",
    )
    cb_gr: bool = Field(
        default=True, description="If markers should be colored by group."
    )
    cb_gr_rand: bool = Field(
        default=False, description="If group color should be generated randomly."
    )
    cb_gr_dict: bool = Field(
        default=False,
        description="If group color should be read from custom dictionary.",
    )
    cb_gr_key: bool = Field(
        default=True, description="If group color should be generated from group key."
    )
    pie_check: bool = Field(
        default=False, description="If markers should be rendered as pie charts."
    )
    scale_check: bool = Field(
        default=False, description="If markers should be scaled by data in CSV column."
    )
    shape_col: bool = Field(
        default=False,
        description="If markers should get their shape from data in CSV column.",
    )
    shape_gr: bool = Field(
        default=True, description="If markers should get their shape from group."
    )
    shape_gr_rand: bool = Field(
        default=True, description="If group shape should be generated randomly."
    )
    shape_gr_dict: bool = Field(
        default=False,
        description="If group shape should be read from custom dictionary.",
    )
    shape_fixed: bool = Field(
        default=False,
        description="If a single fixed shape should be used for all markers.",
    )
    opacity_check: bool = Field(
        default=False,
        description="If markers should get their opacities from data in CSV column.",
    )
    no_outline: bool = Field(
        default=False,
        alias="_no_outline",
        description="If marker shapes should be rendered without outline.",
    )
    no_fill: bool = Field(
        default=False,
        description="If marker shapes should be rendered without filling.",
    )
    collectionItem_col: bool = Field(
        default=False,
        description=(
            "If markers should get their collection item from data in CSV column."
        ),
    )
    collectionItem_fixed: bool = Field(
        default=True,
        description=(
            "If a single fixed collection item should be used for all markers."
        ),
    )
    sortby_check: bool = Field(
        default=False,
        description="If markers should be sorted by data in CSV column.",
    )
    sortby_desc_check: bool = Field(
        default=False,
        description="If markers should be sorted in descending order.",
    )
    edges_check: bool = Field(
        default=False,
        description="If markers should be connected by edges in Network Diagram mode.",
    )


class DropdownOption(SchemaBaseModel):
    # We use extra="allow" here because we want to allow extra keys in the config
    # dictionary. This is because we want to allow the user to add custom keys to the
    # dropdown options, e.g. "expectedHeader.cb_col".
    model_config = ConfigDict(extra="allow")
    optionName: str = Field(description="Name displayed in the dropdown menu.")
    name: str = Field(
        description="Name of the tab to be loaded when the option is selected."
    )


class menuButton(SchemaBaseModel):
    text: Union[list[str], str] = Field(
        description=("Text of the menu item. If list, then a nested menu is created.")
    )
    url: str = Field(description="Url of the menu item.")


class MarkerFile(SchemaBaseModel):
    title: str = Field(description="Name of marker button.")
    comment: Optional[str] = Field(
        default=None,
        description="Optional description text shown next to marker button.",
    )
    name: Optional[str] = Field(default=None, description="Name of marker tab.")
    auto_load: Union[bool, int] = Field(
        default=False,
        alias="autoLoad",
        description=(
            "If the CSV file for the marker dataset should be automatically loaded "
            "when the TMAP project is opened. If this is false, the user instead has "
            "to click on the marker button in the GUI to load the dataset. "
            "If this is an integer, the n-th marker dataset is automatically loaded."
        ),
    )
    hide_settings: bool = Field(
        default=False,
        alias="hideSettings",
        description="Hide markers' settings and add a toggle button instead.",
    )
    uid: Optional[str] = Field(
        default=None,
        description=(
            "A unique identifier used internally by TissUUmaps to reference the marker "
            "dataset."
        ),
    )
    expected_header: ExpectedHeader = Field(alias="expectedHeader")
    expected_radios: ExpectedRadios = Field(
        default_factory=lambda: ExpectedRadios(), alias="expectedRadios"
    )
    path: Union[str, list[str]] = Field(
        description=(
            "Relative file path to CSV file in which marker data is stored. If array "
            "of string, then a dropdown is created instead of a button."
        ),
    )
    dropdown_options: Optional[list[DropdownOption]] = Field(
        default=None,
        alias="dropdownOptions",
        description=(
            "List of dropdown options. Each option is a dictionary with the keys "
            "'title' and 'path'."
        ),
    )
    settings: list[Setting] = []
    from_button: Optional[int] = Field(
        default=None,
        alias="fromButton",
        description=(
            "If this is an integer, then the marker dataset is loaded from the n-th "
            "marker button."
        ),
    )


class RegionFile(SchemaBaseModel):
    title: str = Field(description="Name of region button.")
    comment: Optional[str] = Field(
        default=None,
        description="Optional description text shown next to region button.",
    )
    auto_load: bool = Field(
        default=False,
        alias="autoLoad",
        description=(
            "If the regions should be automatically loaded when the TMAP project is "
            "opened. If this is false, the user instead has to click on the region "
            "button in the GUI to load the regions."
        ),
    )
    path: Union[str, list[str]] = Field(
        description=(
            "Relative file path to GeoJSON file in which marker data is stored. If "
            "array of string, then a dropdown is created instead of a button."
        ),
    )
    settings: list[Setting] = []


class Project(RootSchemaBaseModelV01):
    _previous_model_type: ClassVar[Optional[Type[RootSchemaBaseModel]]] = ProjectV00
    filename: Optional[str] = Field(default=None, description="Name of the project.")
    description: Optional[str] = Field(
        default=None, description="Description of the project. Can contain html tags."
    )
    link: Optional[str] = Field(
        default=None,
        description=(
            "Url to a publication or other external resource: a click on the filename "
            "will open this link."
        ),
    )
    layers: list[Layer] = []
    layer_opacities: dict[int, float] = Field(default={}, alias="layerOpacities")
    layer_visibilities: dict[int, bool] = Field(default={}, alias="layerVisibilities")
    layer_filters: dict[int, list[LayerFilter]] = Field(
        default={},
        alias="layerFilters",
        description="Image filters to be applied to pixels in image layers.",
    )
    filters: list[Filter] = Field(
        default=[Filter.SATURATION, Filter.BRIGHTNESS, Filter.CONTRAST],
        description=(
            "List of filters shown as active filters in the GUI under the Image layers "
            "tab."
        ),
    )
    composite_mode: CompositeMode = Field(
        default=CompositeMode.SOURCE_OVER,
        alias="compositeMode",
        description=(
            "Mode defining how image layers will be merged (composited) with each "
            "other. Valid string values are 'source-over' and 'lighter', which "
            "correspond to 'Channels' and 'Composite' in the GUI."
        ),
    )
    collection_layout: Optional[CollectionLayout] = Field(
        default=None,
        alias="collectionLayout",
        description=(
            "Options to be passed to OpenSeadragon arrange method when in collection"
            "mode. See "
            "(https://openseadragon.github.io/docs/OpenSeadragon.World.html#arrange)"
        ),
    )
    mpp: Optional[float] = Field(
        default=None,
        description=(
            "The image scale in Microns Per Pixels. If not null, then adds a scale bar "
            "to the viewer. Set to 0 to display the scale bar in pixels."
        ),
    )
    bounding_box: Optional[BoundingBox] = Field(
        default=None,
        alias="boundingBox",
        description=(
            "Bounding box used to set initial zoom and pan on the view when loading "
            "the project."
        ),
    )
    rotate: int = Field(
        default=0,
        description=(
            "Angle of rotation of the view in degrees. Only multiples of 90 degrees "
            "are supported."
        ),
    )
    marker_files: list[MarkerFile] = Field(default=[], alias="markerFiles")
    regions: dict[str, Any] = Field(default={}, description="GeoJSON object.")
    region_file: Optional[str] = Field(
        default=None,
        alias="regionFile",
        description=(
            "**[Deprecated]** GeoJSON region file loaded on project initialization. "
            "Use regionFiles instead."
        ),
    )
    region_files: list[RegionFile] = Field(default=[], alias="regionFiles")
    plugins: list[str] = Field(
        default=[], description="List of plugins to load with the project."
    )
    hide_tabs: bool = Field(
        default=False,
        alias="hideTabs",
        description=(
            "Hide tabs of markers dataset. Only use when you have a unique marker tab."
        ),
    )
    hide_channel_range: bool = Field(
        default=False,
        alias="hideChannelRange",
        description=(
            "Hide input range of channels. Only use when you have a unique image layer."
        ),
    )
    hide_navigator: bool = Field(
        default=False,
        alias="hideNavigator",
        description="Hide navigator of the viewer.",
    )
    collection_mode: bool = Field(
        default=False,
        alias="collectionMode",
        description=(
            "If true, then the viewer will be in collection mode, which puts "
            "all layers in a grid next to each other."
        ),
    )
    background_color: Optional[str] = Field(
        default=None,
        alias="backgroundColor",
        description="Background color of the viewer.",
    )
    menu_buttons: Optional[list[menuButton]] = Field(
        default=None,
        alias="menuButtons",
        description="List of menu items to be added to the menu bar.",
    )
    settings: list[Setting] = []

    @classmethod
    def _upgrade_previous(
        cls, previous_model_instance: RootSchemaBaseModel
    ) -> "Project":
        assert isinstance(previous_model_instance, ProjectV00)
        project_data = previous_model_instance.model_dump(
            by_alias=True, exclude={"schema_version"}
        )
        # upgrade markerFiles
        for marker_file_data in project_data["markerFiles"]:
            assert isinstance(marker_file_data, dict)
            old_expected_csv_data: dict[str, Any] = marker_file_data.pop("expectedCSV")
            if "expectedHeader" not in marker_file_data:
                marker_file_data["expectedHeader"] = {}
            expected_header_data = marker_file_data["expectedHeader"]
            if "expectedRadios" not in marker_file_data:
                marker_file_data["expectedRadios"] = {}
            expected_radios_data = marker_file_data["expectedRadios"]
            # uid: None --> "uniquetab"
            if marker_file_data.get("uid") is None:
                marker_file_data["uid"] = "uniquetab"
            # infer name from title
            title_value: str = marker_file_data["title"]
            marker_file_data["name"] = title_value.replace("Download", "").strip()
            # hide settings by default
            marker_file_data["hideSettings"] = True
            # expectedCSV --> expectedHeader/expectedRadios
            expected_header_data["X"] = old_expected_csv_data["X_col"]
            expected_header_data["Y"] = old_expected_csv_data["Y_col"]
            if old_expected_csv_data["key"] == "letters":
                expected_header_data["gb_col"] = old_expected_csv_data.get("group")
                expected_header_data["gb_name"] = old_expected_csv_data.get("name")
            else:
                expected_header_data["gb_col"] = old_expected_csv_data.get("name")
                expected_header_data["gb_name"] = old_expected_csv_data.get("group")
            piechart_value = old_expected_csv_data.get("piechart")
            expected_radios_data["pie_check"] = bool(piechart_value)
            expected_header_data["pie_col"] = piechart_value or None

            color_value = old_expected_csv_data.get("color")
            expected_radios_data["cb_gr"] = not bool(color_value)
            expected_radios_data["cb_col"] = bool(color_value)
            expected_header_data["cb_col"] = color_value or None

            scale_value = old_expected_csv_data.get("scale")
            expected_radios_data["scale_check"] = bool(scale_value)
            expected_header_data["scale_col"] = scale_value or None
            # old settings --> expectedHeader/expectedRadios
            for setting_data in marker_file_data.get("settings", []):
                assert isinstance(setting_data, dict)
                module_value = setting_data["module"]
                function_value = setting_data["function"]
                value_value = setting_data["value"]
                # marker shape
                if module_value == "markerUtils" and function_value == "_randomShape":
                    assert isinstance(
                        value_value, bool
                    ), "The `markerUtils._randomShape` setting value must be a bool"
                    expected_radios_data["shape_fixed"] = not value_value
                    if not value_value:
                        expected_header_data["shape_fixed"] = "square"
                # marker opacity
                if module_value == "glUtils" and function_value == "_markerOpacity":
                    try:
                        value_value = float(value_value)
                    except ValueError:
                        raise AssertionError(
                            "The `glUtils._markerOpacity` setting value must be a float"
                        )
                    setting_data["function"] = "_markerOpacityOld"
                    expected_header_data["opacity"] = value_value
                # marker color
                if (
                    module_value == "markerUtils" and function_value == "_colorsperkey"
                ) or (
                    module_value == "HTMLElementUtils"
                    and function_value in ("_colorsperiter", "_colorsperbarcode")
                ):
                    if isinstance(value_value, str):
                        try:
                            json.loads(value_value)
                        except json.JSONDecodeError:
                            raise AssertionError(
                                "The setting values of `markerUtils._colorsperkey`, "
                                "`HTMLElementUtils._colorsperiter` and "
                                "`HTMLElementUtils._colorsperbarcode` must be JSON"
                            )
                    else:
                        assert isinstance(value_value, (dict, list))
                    expected_radios_data["cb_gr"] = True
                    expected_radios_data["cb_gr_rand"] = False
                    expected_radios_data["cb_gr_key"] = False
                    expected_radios_data["cb_gr_dict"] = True
                    expected_header_data["cb_gr_dict"] = value_value
        return Project.model_validate(project_data)
