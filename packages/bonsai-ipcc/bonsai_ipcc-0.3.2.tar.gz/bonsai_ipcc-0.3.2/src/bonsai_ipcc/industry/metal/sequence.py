import logging

from ..._sequence import Sequence
from . import elementary as elem
from ._data import concordance as conc
from ._data import dimension as dim
from ._data import parameter as par

logger = logging.getLogger(__name__)


def tier1a_co2_coke(
    year=2019, region="DE", cokeprocess_type="by-product_recovery", uncertainty="def"
):
    """Template calculation sequence for tier 1a method.

    CO2 Emissions for coke production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    cokeprocess_type : str
        type of coke production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    #'cao_in_clinker, ckd_correc_fact'
    seq.read_parameter(name="ck", table="ck", coords=[year, region, cokeprocess_type])

    seq.read_parameter(
        name="ef_co2", table="ef_co2_v3c4", coords=[year, region, cokeprocess_type]
    )

    value = seq.elementary.co2_coke_tier1a_(
        ck=seq.step.ck.value, ef_co2=seq.step.ef_co2.value
    )

    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)

    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1a_ch4_coke(
    year=2019, region="DE", cokeprocess_type="by-product_recovery", uncertainty="def"
):
    """Template calculation sequence for tier 1a method.

    CH4 Emissions for coke production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    cokeprocess_type : str
        type of coke production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="ck", table="ck", coords=[year, region, cokeprocess_type])

    seq.read_parameter(
        name="ef_ch4", table="ef_ch4_v3c4", coords=[year, region, cokeprocess_type]
    )

    value = seq.elementary.ch4_coke(ck=seq.step.ck.value, ef_ch4=seq.step.ef_ch4.value)

    seq.store_result(name="ch4_emission", value=value, unit="t/yr", year=year)

    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1b_co2_coke(
    year=2019, region="DE", cokeprocess_type="by-product_recovery", uncertainty="def"
):
    """Template calculation sequence for tier 1b method.

    CO2 Emissions for coke production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    cokeprocess_type : str
        type of coke production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    #'cao_in_clinker, ckd_correc_fact'
    seq.read_parameter(name="ck", table="ck", coords=[year, region, cokeprocess_type])

    seq.read_parameter(name="c_ck", table="c_ck", coords=[year, region])

    seq.read_parameter(name="cc", table="cc", coords=[year, region, cokeprocess_type])

    seq.read_parameter(name="c_cc", table="c_cc", coords=[year, region])

    value = seq.elementary.co2_coke_tier1b_(
        ck=seq.step.ck.value,
        cc=seq.step.cc.value,
        c_ck=seq.step.ck.value,
        c_cc=seq.step.cc.value,
    )

    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)

    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_co2_coke(
    year=2019, region="DE", cokeprocess_type="by-product_recovery", uncertainty="def"
):
    """Template calculation sequence for tier 2 method.

    CO2 Emissions for coke production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    cokeprocess_type : str
        type of coke production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="cc", table="cc", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_cc",
        table="c_cc",
        coords=[year, region],
    )
    seq.read_parameter(name="bg", table="bg", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_bg",
        table="c_bg",
        coords=[year, region],
    )

    seq.read_parameter(name="co", table="co", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_co",
        table="c_co",
        coords=[year, region],
    )
    seq.read_parameter(name="cog", table="cog", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_cog",
        table="c_cog",
        coords=[year, region],
    )
    seq.read_parameter(
        name="e_flaring", table="e_flaring", coords=[year, region, cokeprocess_type]
    )

    # loop over all by-products
    d = seq.get_inventory_levels(table="cob_b", year=year, region=region)
    value = 0.0
    for b in range(len(list(d.values())[0])):
        byproduct_type = d["byproduct_type"][b]

        seq.read_parameter(
            name="cob_b",
            table="cob_b",
            coords=[year, region, cokeprocess_type, byproduct_type],
        )

        seq.read_parameter(
            name="c_b",
            table="c_b",
            coords=[year, region, byproduct_type],
        )
        value += seq.elementary.c_cob(
            cob_b=seq.step.cob_b.value,
            c_b=seq.step.c_b.value,
        )

    seq.store_result(name="c_cob", value=value, unit="t/yr")

    # loop (sum over all process materials)
    d = seq.get_inventory_levels(table="pm_a", year=year, region=region)
    value = 0.0
    for a in range(len(list(d.values())[0])):
        material_type = d["material_type"][a]

        seq.read_parameter(
            name="pm_a",
            table="pm_a",
            coords=[year, region, cokeprocess_type, material_type],
        )

        seq.read_parameter(
            name="c_a",
            table="c_a",
            coords=[year, region, material_type],
        )

        value += seq.elementary.c_pm(
            pm_a=seq.step.pm_a.value,
            c_a=seq.step.c_a.value,
        )
    seq.store_result(name="c_pm", value=value, unit="t/yr")

    value = seq.elementary.co2_coke_tier2_(
        cc=seq.step.cc.value,
        c_cc=seq.step.c_cc.value,
        c_pm=seq.step.c_pm.value,
        bg=seq.step.bg.value,
        c_bg=seq.step.c_bg.value,
        co=seq.step.c_bg.value,
        c_co=seq.step.c_co.value,
        cog=seq.step.cog.value,
        c_cog=seq.step.c_cog.value,
        c_cob=seq.step.c_cob.value,
        e_flaring=seq.step.e_flaring.value,
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier3_co2_coke(
    year=2019,
    region="a specific plant",
    cokeprocess_type="by-product_recovery",
    uncertainty="def",
):
    """Template calculation sequence for tier 3 method. Plant-specific carbon content for materials and by-products required.

    CO2 Emissions for coke production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    cokeprocess_type : str
        type of coke production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="cc", table="cc", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_cc",
        table="c_cc",
        coords=[year, region],
    )
    seq.read_parameter(name="bg", table="bg", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_bg",
        table="c_bg",
        coords=[year, region],
    )

    seq.read_parameter(name="co", table="co", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_co",
        table="c_co",
        coords=[year, region],
    )
    seq.read_parameter(name="cog", table="cog", coords=[year, region, cokeprocess_type])
    seq.read_parameter(
        name="c_cog",
        table="c_cog",
        coords=[year, region],
    )
    seq.read_parameter(
        name="e_flaring", table="e_flaring", coords=[year, region, cokeprocess_type]
    )

    # loop (sum over all process materials)
    d = seq.get_inventory_levels(table="pm_a", year=year, region=region)
    d1 = seq.get_inventory_levels(table="cob_b", year=year, region=region)
    value = 0.0
    for a in range(len(list(d.values())[0])):
        for b in range(len(list(d.values())[0])):
            material_type = d["material_type"][a]
            byproduct_type = d1["byproduct_type"][b]

            seq.read_parameter(
                name="pm_a",
                table="pm_a",
                coords=[year, region, cokeprocess_type, material_type],
            )

            seq.read_parameter(
                name="c_a",
                table="c_a",
                coords=[year, region, material_type],
            )

            seq.read_parameter(
                name="cob_b",
                table="cob_b",
                coords=[year, region, cokeprocess_type, byproduct_type],
            )

            seq.read_parameter(
                name="c_b",
                table="c_b",
                coords=[year, region, byproduct_type],
            )

            value += seq.elementary.co2_coke_tier2_(
                cc=seq.step.cc.value,
                c_cc=seq.step.c_cc.value,
                pm_a=seq.step.pm_a.value,
                c_a=seq.step.c_a.value,
                bg=seq.step.bg.value,
                c_bg=seq.step.c_bg.value,
                co=seq.step.co.value,
                c_co=seq.step.c_co.value,
                cog=seq.step.cog.value,
                c_cog=seq.step.c_cog.value,
                cob_b=seq.step.cob_b.value,
                c_b=seq.step.c_b.value,
                e_flaring=seq.step.e_flaring.value,
            )

    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_steel(year=2019, region="DE", steelmaking_type="bof", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for steel production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    steelmaking_type : str
        type of steel making
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="q", table="q_steel", coords=[year, region, steelmaking_type]
    )
    seq.read_parameter(
        name="ef_co2",
        table="ef2_co2_v3c4",
        coords=[year, region, steelmaking_type],
    )

    value = seq.elementary.co2_steelmaking_tier1_(
        q=seq.step.q.value, ef_co2=seq.step.ef_co2.value
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_pigiron(
    year=2019, region="DE", pigironprocess_type="undefined", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for pig iron production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    pigironprocess_type : str
        pigironprocess type
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="q", table="q_pigiron", coords=[year, region, pigironprocess_type]
    )
    seq.read_parameter(
        name="ef_co2",
        table="ef3_co2_v3c4",
        coords=[year, region, pigironprocess_type],
    )

    value = seq.elementary.co2_pigiron(q=seq.step.q.value, ef_co2=seq.step.ef_co2.value)
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_dri(
    year=2019, region="DE", driprocess_type="undefined", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for direct reduced iron production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    driprocess_type : str
        process type of direct reduced iron production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="q", table="q_dri", coords=[year, region, driprocess_type])
    seq.read_parameter(
        name="ef_co2",
        table="ef4_co2_v3c4",
        coords=[year, region, driprocess_type],
    )

    value = seq.elementary.co2_dri_tier1_(
        q=seq.step.q.value, ef_co2=seq.step.ef_co2.value
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_sinter(
    year=2019, region="DE", sinterprocess_type="undefined", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for sinter production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    sinterprocess_type : str
        process type of sinter production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="q", table="q_sinter", coords=[year, region, sinterprocess_type]
    )
    seq.read_parameter(
        name="ef_co2",
        table="ef5_co2_v3c4",
        coords=[year, region, sinterprocess_type],
    )

    value = seq.elementary.co2_sinter_tier1_(
        q=seq.step.q.value, ef_co2=seq.step.ef_co2.value
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_pellet(
    year=2019, region="DE", pelletprocess_type="undefined", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for iron pellet production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    pelletrprocess_type : str
        process type of iron pellet production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="q", table="q_pellet", coords=[year, region, pelletprocess_type]
    )
    seq.read_parameter(
        name="ef_co2",
        table="ef6_co2_v3c4",
        coords=[year, region, pelletprocess_type],
    )

    value = seq.elementary.co2_pellet(q=seq.step.q.value, ef_co2=seq.step.ef_co2.value)
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_flaring(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions from BFG and LDG flaring.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="q_bfg", table="q_bfg", coords=[year, region])
    seq.read_parameter(name="q_ldg", table="q_ldg", coords=[year, region])
    seq.read_parameter(
        name="r_bfg",
        table="r_bfg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="cc_bfg",
        table="cc_bfg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="r_ldg",
        table="r_ldg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="cc_ldg",
        table="cc_ldg",
        coords=[year, region],
    )

    value = seq.elementary.co2_flaring(
        q_bfg=seq.step.q_bfg.value,
        q_ldg=seq.step.q_ldg.value,
        r_bfg=seq.step.r_bfg.value,
        cc_bfg=seq.step.cc_bfg.value,
        r_ldg=seq.step.r_ldg.value,
        cc_ldg=seq.step.cc_ldg.value,
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_co2_steel(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 2 method.

    CO2 Emissions for steel and iron production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="pc",
        table="pc",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_pc",
        table="c_co",
        coords=[year, region],
    )
    seq.read_parameter(
        name="ci",
        table="ci",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_ci",
        table="c_cc",
        coords=[year, region],
    )
    seq.read_parameter(
        name="l",
        table="l",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_l",
        table="c_l",
        coords=[year, region],
    )
    seq.read_parameter(
        name="d",
        table="d",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_d",
        table="c_d",
        coords=[year, region],
    )
    seq.read_parameter(
        name="ce",
        table="ce",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_ce",
        table="c_ce",
        coords=[year, region],
    )
    seq.read_parameter(
        name="cog",
        table="cog_tier2",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_cog",
        table="c_cog",
        coords=[year, region],
    )
    seq.read_parameter(
        name="s",
        table="s",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_s",
        table="c_s",
        coords=[year, region],
    )
    seq.read_parameter(
        name="ip",
        table="ip",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_ip",
        table="c_ip",
        coords=[year, region],
    )
    seq.read_parameter(
        name="bfg",
        table="bfg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="c_bfg",
        table="c_bg",
        coords=[year, region],
    )

    # loop over all coke oven by-products
    d = seq.get_inventory_levels(table="cob_a_tier2", year=year, region=region)
    value = 0.0
    for a in range(len(list(d.values())[0])):
        byproduct_type = d["byproduct_type"][a]
        seq.read_parameter(
            name="cob_a",
            table="cob_a_tier2",
            coords=[year, region, byproduct_type],
        )
        seq.read_parameter(
            name="c_a",
            table="c_b",
            coords=[year, region, byproduct_type],
        )
        value += seq.elementary.c_cob_a(
            cob_a=seq.step.cob_a.value, c_a=seq.step.c_a.value
        )
    seq.store_result(name="c_cob_a", value=value, unit="t/yr")

    # loop (sum over all input materials)
    d1 = seq.get_inventory_levels(table="o_b", year=year, region=region)
    value = 0.0
    for b in range(len(list(d1.values())[0])):
        material_type = d1["material_type"][b]

        seq.read_parameter(
            name="o_b",
            table="o_b",
            coords=[year, region, material_type],
        )
        seq.read_parameter(
            name="c_b",
            table="c_a",
            coords=[year, region, material_type],
        )
        value += seq.elementary.c_o_b(o_b=seq.step.o_b.value, c_b=seq.step.c_b.value)
    seq.store_result(name="c_o_b", value=value, unit="t/yr")

    value = seq.elementary.co2_steelmaking_tier2_(
        pc=seq.step.pc.value,
        c_pc=seq.step.c_pc.value,
        c_cob_a=seq.step.c_cob_a.value,
        ci=seq.step.ci.value,
        c_ci=seq.step.c_ci.value,
        l=seq.step.l.value,
        c_l=seq.step.c_l.value,
        d=seq.step.d.value,
        c_d=seq.step.c_d.value,
        ce=seq.step.ce.value,
        c_ce=seq.step.c_ce.value,
        c_o_b=seq.step.c_o_b.value,
        cog=seq.step.cog.value,
        c_cog=seq.step.c_cog.value,
        s=seq.step.s.value,
        c_s=seq.step.c_s.value,
        ip=seq.step.ip.value,
        c_ip=seq.step.c_ip.value,
        bfg=seq.step.bfg.value,
        c_bfg=seq.step.c_bfg.value,
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)

    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_ch4_coke(
    year=2019, region="DE", cokeprocess_type="by-product_recovery", uncertainty="def"
):
    """Template calculation sequence for tier 2 method. Country-specific emission factors required!

    CH4 Emissions for coke production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    cokeprocess_type : str
        type of coke production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="ck", table="ck", coords=[year, region, cokeprocess_type])

    seq.read_parameter(
        name="ef_ch4", table="ef_ch4_v3c4", coords=[year, region, cokeprocess_type]
    )

    value = seq.elementary.ch4_coke(ck=seq.step.ck.value, ef_ch4=seq.step.ef_ch4.value)

    seq.store_result(name="ch4_emission", value=value, unit="t/yr", year=year)

    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_co2_sinter(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 2 method.

    CO2 Emissions for sinter production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="cbr", table="cbr", coords=[year, region])
    seq.read_parameter(
        name="c_cbr",
        table="c_co",
        coords=[year, region],
    )
    seq.read_parameter(name="cog", table="cog_tier2", coords=[year, region])
    seq.read_parameter(
        name="c_cog",
        table="c_cog",
        coords=[year, region],
    )
    seq.read_parameter(name="bfg", table="bfg", coords=[year, region])
    seq.read_parameter(
        name="c_bfg",
        table="c_bg",
        coords=[year, region],
    )

    # loop over all materials
    d = seq.get_inventory_levels(table="pm_a_sinter", year=year, region=region)
    value = 0.0
    for a in range(len(list(d.values())[0])):
        material_type = d["material_type"][a]
        seq.read_parameter(
            name="pm_a",
            table="pm_a_sinter",
            coords=[year, region, material_type],
        )
        seq.read_parameter(
            name="c_a",
            table="c_a",
            coords=[year, region, material_type],
        )
        value += seq.elementary.c_pm_a(pm_a=seq.step.pm_a.value, c_a=seq.step.c_a.value)
    seq.store_result(name="c_pm_a", value=value, unit="t/yr")

    value = seq.elementary.co2_sinter_tier2_(
        cbr=seq.step.cbr.value,
        c_cbr=seq.step.c_cbr.value,
        cog=seq.step.cog.value,
        c_cog=seq.step.c_cog.value,
        bfg=seq.step.bfg.value,
        c_bfg=seq.step.c_bfg.value,
        c_pm_a=seq.step.c_pm_a.value,
    )

    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_co2_dri(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 2 method.

    CO2 Emissions for direct reduced iron production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="dri_ng", table="dri_ng", coords=[year, region])
    seq.read_parameter(name="c_ng", table="c_ng", coords=[year, region])
    seq.read_parameter(name="dri_bz", table="dri_bz", coords=[year, region])
    seq.read_parameter(name="c_bz", table="c_bz", coords=[year, region])
    seq.read_parameter(name="dri_ck", table="dri_ck", coords=[year, region])
    seq.read_parameter(name="c_ck", table="c_ck_energ", coords=[year, region])

    value = seq.elementary.co2_dri_tier2_(
        dri_ng=seq.step.dri_ng.value,
        c_ng=seq.step.c_ng.value,
        dri_bz=seq.step.dri_bz.value,
        c_bz=seq.step.c_bz.value,
        dri_ck=seq.step.dri_ck.value,
        c_ck=seq.step.c_ck.value,
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_ch4_sinter(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    CH4 Emissions for sinter production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="si", table="si", coords=[year, region])
    seq.read_parameter(
        name="ef_si",
        table="ef5_ch4_si",
        coords=[year, region],
    )

    value = seq.elementary.ch4_sinter(si=seq.step.si.value, ef_si=seq.step.ef_si.value)
    seq.store_result(name="ch4_emission", value=value, unit="kg/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_ch4_pigiron(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    CH4 Emissions for pig iron production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="pi", table="pi", coords=[year, region])
    seq.read_parameter(
        name="ef_pi",
        table="ef5_ch4_pi",
        coords=[year, region],
    )

    value = seq.elementary.ch4_pigiron(pi=seq.step.pi.value, ef_pi=seq.step.ef_pi.value)
    seq.store_result(name="ch4_emission", value=value, unit="kg/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_ch4_dri(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    CH4 Emissions for steel by direct reduced iron production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="dri", table="dri", coords=[year, region])
    seq.read_parameter(
        name="ef_dri",
        table="ef5_ch4_dri",
        coords=[year, region],
    )

    value = seq.elementary.ch4_dri(dri=seq.step.dri.value, ef_dri=seq.step.ef_dri.value)
    seq.store_result(name="ch4_emission", value=value, unit="kg/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_n2o_flaring(year=2019, region="DE", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    N2O Emissions from BFG and LDG flaring.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(name="q_bfg", table="q_bfg", coords=[year, region])
    seq.read_parameter(name="q_ldg", table="q_ldg", coords=[year, region])
    seq.read_parameter(
        name="r_bfg",
        table="r_bfg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="ef_bfg",
        table="ef_n2o_bfg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="r_ldg",
        table="r_ldg",
        coords=[year, region],
    )
    seq.read_parameter(
        name="ef_ldg",
        table="ef_n2o_ldg",
        coords=[year, region],
    )

    value = seq.elementary.n2o_flaring(
        q_bfg=seq.step.q_bfg.value,
        q_ldg=seq.step.q_ldg.value,
        r_bfg=seq.step.r_bfg.value,
        ef_bfg=seq.step.ef_bfg.value,
        r_ldg=seq.step.r_ldg.value,
        ef_ldg=seq.step.ef_ldg.value,
    )
    seq.store_result(name="n2o_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_ferroalloy(
    year=2019, region="DE", ferroallay_type="ferrosilicon_45perc_si", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for ferroalloy production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    ferroalloy_type : str
        type of ferroalloy
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp", table="mp_ferroalloy", coords=[year, region, ferroallay_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_co2_ferroalloy",
        coords=[year, region, ferroallay_type],
    )

    value = seq.elementary.co2_ferroalloy_tier1_(
        mp=seq.step.mp.value, ef=seq.step.ef.value
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_co2_ferroalloy(
    year=2019, region="DE", ferroalloy_type="ferrosilicon_45perc_si", uncertainty="def"
):
    """Template calculation sequence for tier 2 method.

    CO2 Emissions for ferroalloy production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    ferroalloy_type : str
        type of ferroalloy
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    # loop over all agent types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_agent"
    )
    value = 0.0
    for agent_type in l:
        seq.read_parameter(
            name="m_agent",
            table="m_agent",
            coords=[year, region, ferroalloy_type, agent_type],
        )
        seq.read_parameter(
            name="ef_agent",
            table="ef_agent",
            coords=[year, region, agent_type],
        )
        value += seq.elementary.co2_in_agent_tier2_(
            m=seq.seq.step.m_agent.value, ef=seq.step.ef_agent.value
        )
    seq.store_result(name="co2_in_agent", value=value, unit="t/yr", year=year)

    # loop over all ore types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_ore"
    )
    value = 0.0
    for ore_type in l:
        seq.read_parameter(
            name="m_ore",
            table="m_ore",
            coords=[year, region, ferroalloy_type, ore_type],
        )
        seq.read_parameter(
            name="ccontent_ore",
            table="ccontent_ore",
            coords=[year, region, ore_type],
        )
        value += seq.elementary.co2_in_ore(
            m=seq.seq.step.m_ore.value, ccontent=seq.step.ccontent_ore.value
        )
    seq.store_result(name="co2_in_ore", value=value, unit="t/yr", year=year)

    # loop over all slag types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_slag"
    )
    value = 0.0
    for slag_type in l:
        seq.read_parameter(
            name="m_slag",
            table="m_slag",
            coords=[year, region, ferroalloy_type, slag_type],
        )
        seq.read_parameter(
            name="ccontent_slag",
            table="ccontent_slag",
            coords=[year, region, slag_type],
        )
        value += seq.elementary.co2_in_slag(
            m=seq.seq.step.m_slag.value, ccontent=seq.step.ccontent_slag.value
        )
    seq.store_result(name="co2_in_slag", value=value, unit="t/yr", year=year)

    # loop over all non-product types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_out_non_product"
    )
    value = 0.0
    for non_type in l:
        seq.read_parameter(
            name="m_out_non_product",
            table="m_out_non_product",
            coords=[year, region, ferroalloy_type, non_type],
        )
        seq.read_parameter(
            name="ccontent_out_non_product",
            table="ccontent_out_non_product",
            coords=[year, region, non_type],
        )
        value += seq.elementary.co2_out_non_product(
            m=seq.seq.step.m_out_non_product.value,
            ccontent=seq.step.ccontent_out_non_product.value,
        )
    seq.store_result(name="co2_out_non_product", value=value, unit="t/yr", year=year)

    # loop over all product types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_out_product"
    )
    value = 0.0
    for prod_type in l:
        seq.read_parameter(
            name="m_out_product",
            table="m_out_product",
            coords=[year, region, ferroalloy_type, prod_type],
        )
        seq.read_parameter(
            name="ccontent_out_product",
            table="ccontent_out_product",
            coords=[year, region, prod_type],
        )
        value += seq.elementary.co2_out_product(
            m=seq.seq.step.m_out_product.value,
            ccontent=seq.step.ccontent_out_product.value,
        )
    seq.store_result(name="co2_out_product", value=value, unit="t/yr", year=year)

    value = seq.elementary.co2_ferroalloy_tier2_3_(
        co2_in_agent=seq.step.co2_in_agent.value,
        co2_in_ore=seq.step.co2_in_ore.value,
        co2_in_slag=seq.step.co2_in_slag.value,
        co2_out_product=seq.step.co2_out_product.value,
        co2_out_non_product=seq.step.co2_out_non_product.value,
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier3_co2_ferroalloy(
    year=2019, region="DE", ferroalloy_type="ferrosilicon_45perc_si", uncertainty="def"
):
    """Template calculation sequence for tier 3 method.

    CO2 Emissions for ferroalloy production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    ferroalloy_type : str
        type of ferroalloy
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    # loop over all agent types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_agent"
    )

    value = 0.0
    for agent_type in l:
        seq.read_parameter(
            name="m_agent",
            table="m_agent",
            coords=[year, region, ferroalloy_type, agent_type],
        )
        seq.read_parameter(
            name="f_fix_c",
            table="f_fix_c",
            coords=[year, region, agent_type],
        )
        seq.read_parameter(
            name="f_volatiles",
            table="f_volatiles",
            coords=[year, region, agent_type],
        )
        seq.read_parameter(
            name="c_v",
            table="c_v",
            coords=[year, region, agent_type],
        )
        value_c = seq.elementary.ccontent(
            f_fix_c=seq.step.f_fix_c.value,
            f_volatiles=seq.step.f_volatiles.value,
            c_v=seq.step.c_v.value,
        )
        seq.store_result(name="ccontent_agent", value=value_c, unit="t/t", year=year)

        value += seq.elementary.co2_in_agent_tier3_(
            m=seq.seq.step.m_agent.value, ef=seq.step.ccontent_agent.value
        )
    seq.store_result(name="co2_in_agent", value=value, unit="t/yr", year=year)

    # loop over all ore types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_ore"
    )
    value = 0.0
    for ore_type in l:
        seq.read_parameter(
            name="m_ore",
            table="m_ore",
            coords=[year, region, ferroalloy_type, ore_type],
        )
        seq.read_parameter(
            name="ccontent_ore",
            table="ccontent_ore",
            coords=[year, region, ore_type],
        )
        value += seq.elementary.co2_in_ore(
            m=seq.seq.step.m_ore.value, ccontent=seq.step.ccontent_ore.value
        )
    seq.store_result(name="co2_in_ore", value=value, unit="t/yr", year=year)

    # loop over all slag types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_slag"
    )
    value = 0.0
    for slag_type in l:
        seq.read_parameter(
            name="m_slag",
            table="m_slag",
            coords=[year, region, ferroalloy_type, slag_type],
        )
        seq.read_parameter(
            name="ccontent_slag",
            table="ccontent_slag",
            coords=[year, region, slag_type],
        )
        value += seq.elementary.co2_in_slag(
            m=seq.seq.step.m_slag.value, ccontent=seq.step.ccontent_slag.value
        )
    seq.store_result(name="co2_in_slag", value=value, unit="t/yr", year=year)

    # loop over all non-product types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_out_non_product"
    )
    value = 0.0
    for non_type in l:
        seq.read_parameter(
            name="m_out_non_product",
            table="m_out_non_product",
            coords=[year, region, ferroalloy_type, non_type],
        )
        seq.read_parameter(
            name="ccontent_out_non_product",
            table="ccontent_out_non_product",
            coords=[year, region, non_type],
        )
        value += seq.elementary.co2_out_non_product(
            m=seq.seq.step.m_out_non_product.value,
            ccontent=seq.step.ccontent_out_non_product.value,
        )
    seq.store_result(name="co2_out_non_product", value=value, unit="t/yr", year=year)

    # loop over all product types
    l = seq.get_dimension_levels(
        year, region, ferroalloy_type, uncert=uncertainty, table="m_out_product"
    )
    value = 0.0
    for prod_type in l:
        seq.read_parameter(
            name="m_out_product",
            table="m_out_product",
            coords=[year, region, ferroalloy_type, prod_type],
        )
        seq.read_parameter(
            name="ccontent_out_product",
            table="ccontent_out_product",
            coords=[year, region, prod_type],
        )
        value += seq.elementary.co2_out_product(
            m=seq.seq.step.m_out_product.value,
            ccontent=seq.step.ccontent_out_product.value,
        )
    seq.store_result(name="co2_out_product", value=value, unit="t/yr", year=year)

    value = seq.elementary.co2_ferroalloy_tier2_3_(
        co2_in_agent=seq.step.co2_in_agent.value,
        co2_in_ore=seq.step.co2_in_ore.value,
        co2_in_slag=seq.step.co2_in_slag.value,
        co2_out_product=seq.step.co2_out_product.value,
        co2_out_non_product=seq.step.co2_out_non_product.value,
    )
    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_ch4_ferroalloy(
    year=2019, region="DE", ferroalloy_type="ferrosilicon_45perc_si", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CH4 Emissions for ferroalloy production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    ferroalloy_type : str
        type of ferroalloy
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp_ferroalloy",
        table="mp_ferroallay",
        coords=[year, region, ferroalloy_type],
    )
    seq.read_parameter(
        name="ef_ch4",
        table="ef_ch4_ferroalloy_tier1",
        coords=[year, region, ferroalloy_type],
    )
    value = seq.elementary.ch4_ferroalloy_tier1_(
        mp=seq.seq.step.mp_ferroalloy.value, ef=seq.step.ef_ch4.value
    )
    seq.store_result(name="ch4_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_ch4_ferroalloy(
    year=2019, region="DE", ferroalloy_type="ferrosilicon_45perc_si", uncertainty="def"
):
    """Template calculation sequence for tier 2 method.

    CH4 Emissions for ferroalloy production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    ferroalloy_type : str
        type of ferroalloy
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp_ferroalloy",
        table="mp_ferroalloy",
        coords=[year, region, ferroalloy_type],
    )

    # loop over all agent types
    l = seq.get_dimension_levels(
        year,
        region,
        ferroalloy_type,
        uncert=uncertainty,
        table="furnace_operation_frac",
    )

    value = 0.0
    for furnace_type in l:

        seq.read_parameter(
            name="furnace_operation_frac",
            table="furnace_operation_frac",
            coords=[year, region, ferroalloy_type, furnace_type],
        )

        seq.read_parameter(
            name="ef_ch4",
            table="ef_ch4_ferroalloy_tier2",
            coords=[year, region, ferroalloy_type, furnace_type],
        )
        value += seq.elementary.ch4_ferroalloy_tier2_(
            mp=seq.seq.step.mp_ferroalloy.value,
            ef=seq.step.ef_ch4.value,
            furnace_operation_frac=seq.step.furnace_operation_frac.value,
        )
    seq.store_result(name="ch4_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_alu(year=2019, region="DE", aluprocess_type="prebake", uncertainty="def"):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for alu production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    aluprocess_type : str
        process type of aluminium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp", table="mp_alu", coords=[year, region, aluprocess_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_co2_alu",
        coords=[year, region, aluprocess_type],
    )
    value = seq.elementary.e_co2_tier1_(mp=seq.step.mp.value, ef=seq.step.ef.value)

    seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_co2_alu(
    year=2019, region="DE", aluprocess_type="prebake_cwpb", uncertainty="def"
):
    """Template calculation sequence for tier 2 and 3 method.

    CO2 Emissions for alu production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    aluprocess_type : str
        process type of aluminium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    if "prebake" in aluprocess_type:
        seq.read_parameter(name="nac", table="nac_alu", coords=[year, region])
        seq.read_parameter(
            name="mp", table="mp_alu", coords=[year, region, aluprocess_type]
        )
        seq.read_parameter(name="s_a", table="s_a", coords=[year, region])
        seq.read_parameter(name="ash_a", table="ash_a", coords=[year, region])

        value = seq.elementary.e_co2_anode(
            nac=seq.step.nac.value,
            mp=seq.step.mp.value,
            s_a=seq.step.s_a.value,
            ash_a=seq.step.ash_a.value,
        )

        seq.store_result(name="e_co2_anode", value=value, unit="t/yr", year=year)

        seq.read_parameter(name="ga", table="ga", coords=[year, region])
        seq.read_parameter(name="h_w", table="h_w", coords=[year, region])
        seq.read_parameter(name="ba", table="ba", coords=[year, region])
        seq.read_parameter(name="wt", table="wt", coords=[year, region])

        value = seq.elementary.e_co2_pitch(
            ga=seq.step.ga.value,
            h_w=seq.step.h_w.value,
            ba=seq.step.ba.value,
            wt=seq.step.wt.value,
        )

        seq.store_result(name="e_co2_pitch", value=value, unit="t/yr", year=year)

        seq.read_parameter(name="pcc", table="pcc", coords=[year, region])
        seq.read_parameter(name="s_pc", table="c_pc", coords=[year, region])
        seq.read_parameter(name="ash_pc", table="ash_pc", coords=[year, region])

        value = seq.elementary.e_co2_packing(
            pcc=seq.step.pcc.value,
            ba=seq.step.ba.value,
            s_pc=seq.step.s_pc.value,
            ash_pc=seq.step.ash_pc.value,
        )

        seq.store_result(name="e_co2_packing", value=value, unit="t/yr", year=year)

        value = seq.elementary.e_co2_prebake(
            e_co2_pitch=seq.step.e_co2_pitch.value,
            e_co2_anode=seq.step.e_co2_anode.value,
            e_co2_packing=seq.step.e_co2_packing.value,
        )
        seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)

    elif "soderberg" in aluprocess_type:
        seq.read_parameter(name="pc", table="pc", coords=[year, region])
        seq.read_parameter(
            name="mp", table="mp_alu", coords=[year, region, aluprocess_type]
        )
        seq.read_parameter(
            name="csm", table="csm", coords=[year, region, aluprocess_type]
        )
        seq.read_parameter(name="bc", table="bc", coords=[year, region])
        seq.read_parameter(name="s_p", table="s_p", coords=[year, region])
        seq.read_parameter(name="ash_p", table="ash_p", coords=[year, region])
        seq.read_parameter(name="h_p", table="bh_pc", coords=[year, region])
        seq.read_parameter(name="s_c", table="s_c", coords=[year, region])
        seq.read_parameter(name="ash_c", table="ash_c", coords=[year, region])
        seq.read_parameter(name="cd", table="cd", coords=[year, region])
        value = seq.elementary.e_co2_soderberg(
            pc=seq.step.pc.value,
            mp=seq.step.mp.value,
            csm=seq.step.csm.value,
            bc=seq.step.bc.value,
            s_p=seq.step.s_p.value,
            ash_p=seq.step.ash_p.value,
            h_p=seq.step.h_p.value,
            s_c=seq.step.s_c.value,
            ash_c=seq.step.ash_c.value,
            cd=seq.step.cd.value,
        )
        seq.store_result(name="co2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_cf4_alu(
    year=2019, region="DE", aluprocess_type="prebake_cwpb", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CF4 Emissions for alu production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    aluprocess_type : str
        process type of aluminium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp", table="mp_alu", coords=[year, region, aluprocess_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_cf4_alu",
        coords=[year, region, aluprocess_type],
    )
    value = seq.elementary.e_cf4_tier1_(mp=seq.step.mp.value, ef=seq.step.ef.value)

    seq.store_result(name="CF4_emission", value=value, unit="kg/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_c2f6_alu(
    year=2019, region="DE", aluprocess_type="prebake_cwpb", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    C2F6 Emissions for alu production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    aluprocess_type : str
        process type of aluminium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp", table="mp_alu", coords=[year, region, aluprocess_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_c2f6_alu",
        coords=[year, region, aluprocess_type],
    )
    value = seq.elementary.e_c2f6_tier1_(mp=seq.step.mp.value, ef=seq.step.ef.value)

    seq.store_result(name="C2F6_emission", value=value, unit="kg/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier2_3_pfc_alu(
    year=2019, region="DE", aluprocess_type="prebake_cwpb", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CF4 and C2F6 Emissions for alu production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    aluprocess_type : str
        process type of aluminium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mp", table="mp_alu", coords=[year, region, aluprocess_type]
    )
    seq.read_parameter(
        name="s",
        table="s_cf4_alu",
        coords=[year, region, aluprocess_type],
    )
    seq.read_parameter(
        name="aem",
        table="aem",
        coords=[year, region, aluprocess_type],
    )
    value = seq.elementary.e_cf4_tier2_3_(
        mp=seq.step.mp.value, s=seq.step.s.value, aem=seq.step.aem.value
    )

    seq.store_result(name="CF4_emission", value=value, unit="kg/yr", year=year)

    seq.read_parameter(
        name="f",
        table="f_alu",
        coords=[year, region, aluprocess_type],
    )

    value = seq.elementary.e_c2f6_tier2_3_(
        e_cf4=seq.step.CF4_emission.value, f=seq.step.f.value
    )
    seq.store_result(name="C2F6_emission", value=value, unit="kg/yr", year=year)

    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_2_co2_magnesium(
    year=2019, region="DE", carbonate_type="dolomite", uncertainty="def"
):
    """Template calculation sequence for tier 1 and tier 2 method.

    CO2 Emissions for primary magnesium production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    carbonate_type : str
        carbonate type used as raw material for magnesium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="p", table="p_magnesium", coords=[year, region, carbonate_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_co2_magnesium",
        coords=[year, region, carbonate_type],
    )
    value = seq.elementary.e_co2_magnesium(p=seq.step.p.value, ef=seq.step.ef.value)

    seq.store_result(name="CO2_emission", value=value, unit="Gg/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_sf6_magnesium(
    year=2019, region="DE", carbonate_type="dolomite", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    SF6 Emissions for primary magnesium production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    carbonate_type : str
        carbonate type used as raw material for magnesium production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="mg_c", table="mg_c_magnesium", coords=[year, region, carbonate_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_sf6_magnesium",
        coords=[year, region, carbonate_type],
    )
    value = seq.elementary.e_sf6_magnesium(p=seq.step.p.value, ef=seq.step.ef.value)

    seq.store_result(name="SF6_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_lead(
    year=2019, region="DE", leadprocess_type="default", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for lead production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    leadprocess_type : str
        process type for lead production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="q", table="q_lead", coords=[year, region, leadprocess_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_co2_lead",
        coords=[year, region, leadprocess_type],
    )
    value = seq.elementary.e_co2_lead(q=seq.step.q.value, ef=seq.step.ef.value)

    seq.store_result(name="CO2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step


def tier1_co2_zinc(
    year=2019, region="DE", zincprocess_type="default", uncertainty="def"
):
    """Template calculation sequence for tier 1 method.

    CO2 Emissions for lead production.
    Each step either calls an elementary equation, calls a parameter,
    or performs a simple operation like a loop or a conditional.
    Each step delivers one return value and unit to the list of variables.

    Argument
    ---------
    year : int
        year under study
    region : str
        region under study
    zincprocess_type : str
        process type for zinc production
    uncertainty : str
        'analytical', 'monte_carlo' or a property dimension, e.g. 'def'

    Returns
    -------
    VALUE: DataClass
        Inlcudes the results of each step of the sequence.
    """

    # Initalize variable instance
    seq = Sequence(dim, par, elem, conc, uncert=uncertainty)
    logger.info("Metal sequence started --->")
    seq.store_signature(locals())

    seq.read_parameter(
        name="q", table="q_zinc", coords=[year, region, zincprocess_type]
    )
    seq.read_parameter(
        name="ef",
        table="ef_co2_zinc",
        coords=[year, region, zincprocess_type],
    )
    value = seq.elementary.e_co2_zinc(q=seq.step.q.value, ef=seq.step.ef.value)

    seq.store_result(name="CO2_emission", value=value, unit="t/yr", year=year)
    logger.info("---> Metal sequence finalized.")
    return seq.step
