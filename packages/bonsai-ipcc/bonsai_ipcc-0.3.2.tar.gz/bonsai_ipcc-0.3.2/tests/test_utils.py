import os
from pathlib import Path

import pandas as pd
import pytest

import bonsai_ipcc

TEST_DATA_PATH = Path(os.path.dirname(__file__)) / "data/"

from bonsai_ipcc._sequence import Sequence
from bonsai_ipcc.industry.metal import elementary as elem
from bonsai_ipcc.industry.metal._data import concordance as conc
from bonsai_ipcc.industry.metal._data import dimension as dim
from bonsai_ipcc.industry.metal._data import parameter as par

# myipcc = IPCC()
# year,region,ferroalloy_type,agent_type,property,value,unit
# 2019,DE,ferrosilicon_45perc_si,a,def,100.0,t/yr
# 2019,DE,silicon_metal,b,def,50.0,t/yr
# 2019,DE,ferrosilicon_45perc_si,b,def,50.0,t/yr
# 2019,IT,ferrosilicon_45perc_si,b,def,50.0,t/yr
# 2019,DE,ferrosilicon_45perc_si,b,max,50.0,t/yr


bonsai_ipcc.industry.metal.dimension.agent_type = pd.DataFrame(
    {"code": ["a", "b"], "description": ["test a", "test b"]}
).set_index(["code"])

bonsai_ipcc.industry.metal.parameter.m_agent = pd.DataFrame(
    {
        "year": [2019, 2019, 2019, 2019, 2019],
        "region": ["DE", "DE", "DE", "IT", "DE"],
        "ferroalloy_type": [
            "ferrosilicon_45perc_si",
            "silicon_metal",
            "ferrosilicon_45perc_si",
            "ferrosilicon_45perc_si",
            "ferrosilicon_45perc_si",
        ],
        "agent_type": ["a", "b", "b", "b", "b"],
        "property": ["def", "def", "def", "def", "max"],
        "value": [100.0, 50.0, 50.0, 50.0, 1000000.0],
        "unit": ["t/yr", "t/yr", "t/yr", "t/yr", "t/yr"],
    }
).set_index(["year", "region", "ferroalloy_type", "agent_type", "property"])

bonsai_ipcc.industry.metal.parameter.ef_agent = pd.DataFrame(
    {
        "year": [2019, 2019, 2019, 2019],
        "region": ["DE", "DE", "IT", "IT"],
        "agent_type": ["a", "b", "a", "b"],
        "property": ["def", "def", "def", "def"],
        "value": [1.0, 2.0, 50.0, 50.0],
        "unit": ["t/t", "t/t", "t/t", "t/t"],
    }
).set_index(["year", "region", "agent_type", "property"])


def test_get_dimension_levels_one(
    tables=["m_agent", "ef_agent"],
    uncert="def",
    year=2019,
    region="DE",
    ferroalloy_type="silicon_metal",
):

    seq = Sequence(dim, par, elem, conc, uncert="def")
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncert, table=tables[0]
    )

    value = 0.0
    for a in l:
        seq.read_parameter(
            name=tables[0],
            table=tables[0],
            coords=[year, region, ferroalloy_type, a],
        )
        seq.read_parameter(
            name=tables[1],
            table=tables[1],
            coords=[year, region, a],
        )
        value += seq.elementary.co2_in_agent_tier2_(
            m=seq.step.m_agent.value, ef=seq.step.ef_agent.value
        )
    assert l == ["b"]
    assert value == 100.0


def test_get_dimension_levels_multiple(
    tables=["m_agent", "ef_agent"],
    uncert="def",
    year=2019,
    region="DE",
    ferroalloy_type="ferrosilicon_45perc_si",
):

    seq = Sequence(dim, par, elem, conc, uncert="def")
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncert, table=tables[0]
    )

    value = 0.0
    for a in l:
        seq.read_parameter(
            name=tables[0],
            table=tables[0],
            coords=[year, region, ferroalloy_type, a],
        )
        seq.read_parameter(
            name=tables[1],
            table=tables[1],
            coords=[year, region, a],
        )
        value += seq.elementary.co2_in_agent_tier2_(
            m=seq.step.m_agent.value, ef=seq.step.ef_agent.value
        )
    assert l == ["a", "b"]
    assert value == 200.0
