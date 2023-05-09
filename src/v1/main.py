import streamlit as st
import utils.curves as curves
import polars as pl
import altair as alt
from typing import Callable

st.set_page_config(
    page_title="Ark EXP Calculator",
    page_icon=r"🦕",
    layout="wide",
)

st.markdown(
    "An EXP Calculator for the game 'Ark Survival Evolved.'\n"
    "This is a simple calculator that will take a base amount of EXP you want to start with and will apply a curve to it.\n"
    "The output will be a table of levels and the amount of EXP required to reach that level.\n"
    "As well as a string you can copy into the INI file for the game.\n\n"
    "For reference, the default EXP curve can be found [here.](https://ark.fandom.com/wiki/Leveling#Character_Levels)"
)

st.sidebar.success("Configure your EXP Curve")

### ### ### ### ### ### ###
### STATE MANAGEMENT ###
if "base_exp" not in st.session_state:
    st.session_state.base_exp = 15
if "levels" not in st.session_state:
    st.session_state.levels = 255

levels = st.sidebar.number_input(
    label="Max Level",
    min_value=50,
    max_value=9001,
    value=st.session_state.levels,
    step=1,  # this will allow the slider to adjust the value continuously
)
st.session_state.levels = levels

base_exp: int = st.sidebar.number_input(
    label="Base EXP Points",
    value=st.session_state.base_exp,
)
st.session_state.base_exp: int = base_exp
### END STATE MANAGEMENT ###
### ### ### ### ### ### ###

ARK_LEVEL_STRING = "ExperiencePointsForLevel[{}]={}"
level_curve: list[int] = list(range(1, st.session_state.levels))

curves_info = {
    "📈 Linear Method": {"method": curves.linear_curve},
    "🦖 Quadratic Method": {"method": curves.quadratic_curve},
    "🟦 Cubic Method": {"method": curves.cubic_curve},
    "⤴ Exponential Method": {"method": curves.exponential_curve},
    "⬜ Square Root Method": {"method": curves.sqrt_curve},
    "〽 Logarithmic Method": {"method": curves.log_curve},
    "➿ Fibonacci Method": {"method": curves.fibonacci_curve},
    "📉 Sigmoid Method": {"method": curves.sigmoid_curve},
    "🧩 Piecewise Method": {"method": curves.piecewise_curve},
}
tab_names = (name for name in curves_info)
(
    linear_tab,
    quadratic_tab,
    cubic_tab,
    exponential_tab,
    sqrt_tab,
    log_tab,
    fibonacci_tab,
    sigmoid_tab,
    piecewise_tab,
) = st.tabs(list(tab_names))
# add tabs to the dict now that we know the order
for tab, (_name, info) in zip(
    (linear_tab, quadratic_tab, cubic_tab, exponential_tab, sqrt_tab, log_tab, fibonacci_tab, sigmoid_tab, piecewise_tab),
    curves_info.items(),
):
    info["tab"] = tab


def create_data(curve_method: Callable[[int, int], int]) -> pl.DataFrame:
    data = pl.DataFrame({"Level": level_curve, "XP": [curve_method(i, st.session_state.base_exp) for i in level_curve]})
    return data


def generate_ini_string_exp(data: pl.DataFrame) -> str:
    ark_strings = []
    for i, row in enumerate(data.to_pandas().itertuples(), 1):
        if i == 1:
            ark_strings.append(f"LevelExperienceRampOverrides=({ARK_LEVEL_STRING.format(row.Level, row.XP)},")
        elif i == len(data):
            ark_strings.append(f"{ARK_LEVEL_STRING.format(row.Level, row.XP)})")
        else:
            ark_strings.append(f"{ARK_LEVEL_STRING.format(row.Level, row.XP)},")
    return "\n".join(ark_strings)


def generate_alt_chart_exp(data: pl.DataFrame) -> alt.Chart:
    chart = alt.Chart(data.to_pandas()).mark_line(point=True).encode(x="Level", y="XP")
    return chart


def process_curve(tab, curve_name, curve_function) -> None:
    with tab:
        ini_expander = st.expander("See INI Code")
        st.header(curve_name)
        data = create_data(curve_function)

        # Generate the ARK level strings for each level
        ark_strings = generate_ini_string_exp(data)
        ini_expander.code(ark_strings, language="ini")

        chart = generate_alt_chart_exp(data)
        table_data = data.with_columns(pl.col("XP").cumsum().alias("XP Total"))
        st.write(chart)
        exp_expander = st.expander("See EXP Table")
        exp_expander.table(table_data.to_pandas())
    return


for curve_name, curve_info in curves_info.items():
    process_curve(curve_info["tab"], curve_name, curve_info["method"])
