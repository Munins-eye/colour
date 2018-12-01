#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate Plots
==============
"""

from __future__ import division, unicode_literals

import matplotlib.pyplot as plt
import numpy as np
import os

import colour
from colour.plotting import *
from colour.plotting.diagrams import (
    plot_spectral_locus, plot_chromaticity_diagram_colours,
    plot_chromaticity_diagram, plot_spds_in_chromaticity_diagram)
from colour.plotting.models import (
    plot_RGB_colourspaces_in_chromaticity_diagram,
    RGB_chromaticity_coordinates_chromaticity_diagram_plot,
    ellipses_MacAdam1942_chromaticity_diagram_plot)
from colour.plotting.quality import colour_quality_bars_plot
from colour.plotting.temperature import (
    planckian_locus_plot, planckian_locus_chromaticity_diagram_plot)
from colour.utilities import domain_range_scale

__copyright__ = 'Copyright (C) 2013-2018 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['generate_documentation_plots']


def generate_documentation_plots(output_directory):
    """
    Generates documentation plots.

    Parameters
    ----------
    output_directory : unicode
        Output directory.
    """

    colour.utilities.filter_warnings()

    colour_style()

    np.random.seed(0)

    # *************************************************************************
    # "README.rst"
    # *************************************************************************
    arguments = {
        'tight_layout':
            True,
        'transparent_background':
            True,
        'filename':
            os.path.join(output_directory,
                         'Examples_Plotting_Visible_Spectrum.png')
    }
    plot_visible_spectrum('CIE 1931 2 Degree Standard Observer', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Examples_Plotting_Illuminant_F1_SPD.png')
    plot_single_illuminant_spd('F1', **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Examples_Plotting_Blackbodies.png')
    blackbody_spds = [
        colour.spd_blackbody(i, colour.SpectralShape(0, 10000, 10))
        for i in range(1000, 15000, 1000)
    ]
    plot_multi_spds(
        blackbody_spds,
        y_label='W / (sr m$^2$) / m',
        use_spds_colours=True,
        normalise_spds_colours=True,
        legend_location='upper right',
        bounding_box=(0, 1250, 0, 2.5e15),
        **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Examples_Plotting_Cone_Fundamentals.png')
    plot_single_cmfs(
        'Stockman & Sharpe 2 Degree Cone Fundamentals',
        y_label='Sensitivity',
        bounding_box=(390, 870, 0, 1.1),
        **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Examples_Plotting_Luminous_Efficiency.png')
    mesopic_luminous_efficiency_function = (
        colour.mesopic_luminous_efficiency_function(0.2))
    plot_multi_spds(
        (mesopic_luminous_efficiency_function,
         colour.PHOTOPIC_LEFS['CIE 1924 Photopic Standard Observer'],
         colour.SCOTOPIC_LEFS['CIE 1951 Scotopic Standard Observer']),
        y_label='Luminous Efficiency',
        legend_location='upper right',
        y_tighten=True,
        margins=(0, 0, 0, .1),
        **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Examples_Plotting_BabelColor_Average.png')
    plot_multi_spds(
        colour.COLOURCHECKERS_SPDS['BabelColor Average'].values(),
        use_spds_colours=True,
        title=('BabelColor Average - '
               'Spectral Power Distributions'),
        **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Examples_Plotting_ColorChecker_2005.png')
    plot_single_colour_checker(
        'ColorChecker 2005', text_parameters={'visible': False}, **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Examples_Plotting_Chromaticities_Prediction.png')
    plot_corresponding_chromaticities_prediction(2, 'Von Kries', 'Bianco',
                                                 **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Examples_Plotting_CCT_CIE_1960_UCS_Chromaticity_Diagram.png')
    planckian_locus_chromaticity_diagram_plot_CIE1960UCS(['A', 'B', 'C'],
                                                         **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Examples_Plotting_Chromaticities_CIE_1931_Chromaticity_Diagram.png')
    RGB = np.random.random((32, 32, 3))
    RGB_chromaticity_coordinates_chromaticity_diagram_plot_CIE1931(
        RGB,
        'ITU-R BT.709',
        colourspaces=['ACEScg', 'S-Gamut'],
        show_pointer_gamut=True,
        **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Examples_Plotting_CRI.png')
    single_spd_colour_rendering_index_bars_plot(colour.ILLUMINANTS_SPDS['F2'],
                                                **arguments)

    # *************************************************************************
    # Documentation
    # *************************************************************************
    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_CVD_Simulation_Machado2009.png')
    plot_cvd_simulation_Machado2009(RGB, **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Single_Colour_Checker.png')
    plot_single_colour_checker('ColorChecker 2005', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Multi_Colour_Checkers.png')
    plot_multi_colour_checkers(['ColorChecker 1976', 'ColorChecker 2005'],
                              **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Single_SPD.png')
    data = {
        500: 0.0651,
        520: 0.0705,
        540: 0.0772,
        560: 0.0870,
        580: 0.1128,
        600: 0.1360
    }
    spd = colour.SpectralPowerDistribution(data, name='Custom')
    plot_single_spd(spd, **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Multi_SPDs.png')
    data_1 = {
        500: 0.004900,
        510: 0.009300,
        520: 0.063270,
        530: 0.165500,
        540: 0.290400,
        550: 0.433450,
        560: 0.594500
    }
    data_2 = {
        500: 0.323000,
        510: 0.503000,
        520: 0.710000,
        530: 0.862000,
        540: 0.954000,
        550: 0.994950,
        560: 0.995000
    }
    spd1 = colour.SpectralPowerDistribution(data_1, name='Custom 1')
    spd2 = colour.SpectralPowerDistribution(data_2, name='Custom 2')
    plot_multi_spds([spd1, spd2], **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Single_CMFS.png')
    plot_single_cmfs('CIE 1931 2 Degree Standard Observer', **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Multi_CMFS.png')
    cmfs = ('CIE 1931 2 Degree Standard Observer',
            'CIE 1964 10 Degree Standard Observer')
    plot_multi_cmfs(cmfs, **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Single_Illuminant_SPD.png')
    plot_single_illuminant_spd('A', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Multi_Illuminant_SPDs.png')
    plot_multi_illuminant_spds(['A', 'B', 'C'], **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Visible_Spectrum.png')
    plot_visible_spectrum(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Single_Lightness_Function.png')
    plot_single_lightness_function('CIE 1976', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Multi_Lightness_Functions.png')
    plot_multi_lightness_functions(['CIE 1976', 'Wyszecki 1963'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Single_Luminance_Function.png')
    plot_single_luminance_function('CIE 1976', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Multi_Luminance_Functions.png')
    plot_multi_luminance_functions(['CIE 1976', 'Newhall 1943'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Blackbody_Spectral_Radiance.png')
    plot_blackbody_spectral_radiance(
        3500, blackbody='VY Canis Major', **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Blackbody_Colours.png')
    plot_blackbody_colours(colour.SpectralShape(150, 12500, 50), **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Single_Colour_Swatch.png')
    RGB = ColourSwatch(RGB=(0.32315746, 0.32983556, 0.33640183))
    plot_single_colour_swatch(RGB, **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Multi_Colour_Swatches.png')
    RGB_1 = ColourSwatch(RGB=(0.45293517, 0.31732158, 0.26414773))
    RGB_2 = ColourSwatch(RGB=(0.77875824, 0.57726450, 0.50453169))
    plot_multi_colour_swatches([RGB_1, RGB_2], **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Single_Function.png')
    plot_single_function(lambda x: x ** (1 / 2.2), **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Single_Function.png')
    functions = {
        'Gamma 2.2': lambda x: x ** (1 / 2.2),
        'Gamma 2.4': lambda x: x ** (1 / 2.4),
        'Gamma 2.6': lambda x: x ** (1 / 2.6),
    }
    plot_multi_functions(functions)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Image.png')
    path = os.path.join(colour.__path__[0], '..', 'docs', '_static',
                        'Logo_Medium_001.png')
    plot_image(colour.read_image(str(path)), **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_Corresponding_Chromaticities_Prediction.png')
    plot_corresponding_chromaticities_prediction(1, 'Von Kries', 'CAT02',
                                                 **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Spectral_Locus.png')
    plot_spectral_locus(spectral_locus_colours='RGB', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Chromaticity_Diagram_Colours.png')
    plot_chromaticity_diagram_colours(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Chromaticity_Diagram.png')
    plot_chromaticity_diagram(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Chromaticity_Diagram_CIE1931.png')
    plot_chromaticity_diagram_CIE1931(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Chromaticity_Diagram_CIE1960UCS.png')
    plot_chromaticity_diagram_CIE1960UCS(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_Chromaticity_Diagram_CIE1976UCS.png')
    plot_chromaticity_diagram_CIE1976UCS(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Plot_SPDS_In_Chromaticity_Diagram.png')
    A = colour.ILLUMINANTS_SPDS['A']
    D65 = colour.ILLUMINANTS_SPDS['D65']
    plot_spds_in_chromaticity_diagram([A, D65], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_SPDS_In_Chromaticity_Diagram_CIE1931.png')
    plot_spds_in_chromaticity_diagram_CIE1931([A, D65], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_SPDS_In_Chromaticity_Diagram_CIE1960UCS.png')
    plot_spds_in_chromaticity_diagram_CIE1960UCS([A, D65], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_SPDS_In_Chromaticity_Diagram_CIE1976UCS.png')
    plot_spds_in_chromaticity_diagram_CIE1976UCS([A, D65], **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Plot_Pointer_Gamut.png')
    plot_pointer_gamut(**arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_RGB_Colourspaces_In_Chromaticity_Diagram.png')
    plot_RGB_colourspaces_in_chromaticity_diagram(
        ['ITU-R BT.709', 'ACEScg', 'S-Gamut'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_RGB_Colourspaces_In_Chromaticity_Diagram_CIE1931.png')
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(
        ['ITU-R BT.709', 'ACEScg', 'S-Gamut'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_RGB_Colourspaces_In_'
        'Chromaticity_Diagram_CIE1960UCS.png')
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1960UCS(
        ['ITU-R BT.709', 'ACEScg', 'S-Gamut'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Plot_RGB_Colourspaces_In_'
        'Chromaticity_Diagram_CIE1976UCS.png')
    plot_RGB_colourspaces_in_chromaticity_diagram_CIE1976UCS(
        ['ITU-R BT.709', 'ACEScg', 'S-Gamut'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_RGB_Chromaticity_Coordinates_Chromaticity_Diagram_Plot.png')
    RGB = np.random.random((128, 128, 3))
    RGB_chromaticity_coordinates_chromaticity_diagram_plot(
        RGB, 'ITU-R BT.709', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_RGB_Chromaticity_Coordinates_'
        'Chromaticity_Diagram_Plot_CIE1931.png')
    RGB_chromaticity_coordinates_chromaticity_diagram_plot_CIE1931(
        RGB, 'ITU-R BT.709', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_RGB_Chromaticity_Coordinates_'
        'Chromaticity_Diagram_Plot_CIE1960UCS.png')
    RGB_chromaticity_coordinates_chromaticity_diagram_plot_CIE1960UCS(
        RGB, 'ITU-R BT.709', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_RGB_Chromaticity_Coordinates_'
        'Chromaticity_Diagram_Plot_CIE1976UCS.png')
    RGB_chromaticity_coordinates_chromaticity_diagram_plot_CIE1976UCS(
        RGB, 'ITU-R BT.709', **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Ellipses_MacAdam1942_'
                                         'Chromaticity_Diagram_Plot.png')
    ellipses_MacAdam1942_chromaticity_diagram_plot(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Ellipses_MacAdam1942_'
        'Chromaticity_Diagram_Plot_CIE1931.png')
    ellipses_MacAdam1942_chromaticity_diagram_plot_CIE1931(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Ellipses_MacAdam1942_'
        'Chromaticity_Diagram_Plot_CIE1960UCS.png')
    ellipses_MacAdam1942_chromaticity_diagram_plot_CIE1960UCS(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Ellipses_MacAdam1942_'
        'Chromaticity_Diagram_Plot_CIE1976UCS.png')
    ellipses_MacAdam1942_chromaticity_diagram_plot_CIE1976UCS(**arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Single_CCTF_Plot.png')
    single_cctf_plot('ITU-R BT.709', **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Multi_CCTF_Plot.png')
    multi_cctf_plot(['ITU-R BT.709', 'sRGB'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Single_Munsell_Value_Function_Plot.png')
    single_munsell_value_function_plot('ASTM D1535-08', **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Multi_Munsell_Value_Function_Plot.png')
    multi_munsell_value_function_plot(['ASTM D1535-08', 'McCamy 1987'],
                                      **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Single_Rayleigh_Scattering_SPD_Plot.png')
    single_rayleigh_scattering_spd_plot(**arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_The_Blue_Sky_Plot.png')
    the_blue_sky_plot(**arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_Colour_Quality_Bars_Plot.png')
    illuminant = colour.ILLUMINANTS_SPDS['F2']
    light_source = colour.LIGHT_SOURCES_SPDS['Kinoton 75P']
    light_source = light_source.copy().align(colour.SpectralShape(360, 830, 1))
    cqs_i = colour.colour_quality_scale(illuminant, additional_data=True)
    cqs_l = colour.colour_quality_scale(light_source, additional_data=True)
    colour_quality_bars_plot([cqs_i, cqs_l], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Single_SPD_Colour_Rendering_Index_Bars_Plot.png')
    illuminant = colour.ILLUMINANTS_SPDS['F2']
    single_spd_colour_rendering_index_bars_plot(illuminant, **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Multi_Spd_Colour_Rendering_Index_Bars_Plot.png')
    light_source = colour.LIGHT_SOURCES_SPDS['Kinoton 75P']
    multi_spd_colour_rendering_index_bars_plot([illuminant, light_source],
                                               **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Single_SPD_Colour_Quality_Scale_Bars_Plot.png')
    illuminant = colour.ILLUMINANTS_SPDS['F2']
    single_spd_colour_quality_scale_bars_plot(illuminant, **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Multi_Spd_Colour_Quality_Scale_Bars_Plot.png')
    light_source = colour.LIGHT_SOURCES_SPDS['Kinoton 75P']
    multi_spd_colour_quality_scale_bars_plot([illuminant, light_source],
                                             **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_Planckian_Locus_Plot.png')
    planckian_locus_plot(**arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Planckian_Locus_Chromaticity_Diagram_Plot.png')
    planckian_locus_chromaticity_diagram_plot(['A', 'B', 'C'], **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Planckian_Locus_Chromaticity_Diagram_Plot_CIE1931.png')
    planckian_locus_chromaticity_diagram_plot_CIE1931(['A', 'B', 'C'],
                                                      **arguments)

    arguments['filename'] = os.path.join(
        output_directory,
        'Plotting_Planckian_Locus_Chromaticity_Diagram_Plot_CIE1960UCS.png')
    planckian_locus_chromaticity_diagram_plot_CIE1960UCS(['A', 'B', 'C'],
                                                         **arguments)
    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_RGB_Colourspaces_Gamuts_Plot.png')
    RGB_colourspaces_gamuts_plot(['ITU-R BT.709', 'ACEScg', 'S-Gamut'],
                                 **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Plotting_RGB_Colourspaces_Gamuts_Plot.png')
    RGB_colourspaces_gamuts_plot(['ITU-R BT.709', 'ACEScg', 'S-Gamut'],
                                 **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Plotting_RGB_Scatter_Plot.png')
    RGB_scatter_plot(RGB, 'ITU-R BT.709', **arguments)

    # *************************************************************************
    # "tutorial.rst"
    # *************************************************************************
    arguments['filename'] = os.path.join(output_directory,
                                         'Tutorial_Visible_Spectrum.png')
    plot_visible_spectrum(**arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Tutorial_Sample_SPD.png')
    sample_spd_data = {
        380: 0.048,
        385: 0.051,
        390: 0.055,
        395: 0.060,
        400: 0.065,
        405: 0.068,
        410: 0.068,
        415: 0.067,
        420: 0.064,
        425: 0.062,
        430: 0.059,
        435: 0.057,
        440: 0.055,
        445: 0.054,
        450: 0.053,
        455: 0.053,
        460: 0.052,
        465: 0.052,
        470: 0.052,
        475: 0.053,
        480: 0.054,
        485: 0.055,
        490: 0.057,
        495: 0.059,
        500: 0.061,
        505: 0.062,
        510: 0.065,
        515: 0.067,
        520: 0.070,
        525: 0.072,
        530: 0.074,
        535: 0.075,
        540: 0.076,
        545: 0.078,
        550: 0.079,
        555: 0.082,
        560: 0.087,
        565: 0.092,
        570: 0.100,
        575: 0.107,
        580: 0.115,
        585: 0.122,
        590: 0.129,
        595: 0.134,
        600: 0.138,
        605: 0.142,
        610: 0.146,
        615: 0.150,
        620: 0.154,
        625: 0.158,
        630: 0.163,
        635: 0.167,
        640: 0.173,
        645: 0.180,
        650: 0.188,
        655: 0.196,
        660: 0.204,
        665: 0.213,
        670: 0.222,
        675: 0.231,
        680: 0.242,
        685: 0.251,
        690: 0.261,
        695: 0.271,
        700: 0.282,
        705: 0.294,
        710: 0.305,
        715: 0.318,
        720: 0.334,
        725: 0.354,
        730: 0.372,
        735: 0.392,
        740: 0.409,
        745: 0.420,
        750: 0.436,
        755: 0.450,
        760: 0.462,
        765: 0.465,
        770: 0.448,
        775: 0.432,
        780: 0.421
    }

    spd = colour.SpectralPowerDistribution(sample_spd_data, name='Sample')
    plot_single_spd(spd, **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Tutorial_SPD_Interpolation.png')
    spd_copy = spd.copy()
    spd_copy.interpolate(colour.SpectralShape(400, 770, 1))
    plot_multi_spds(
        [spd, spd_copy], bounding_box=[730, 780, 0.25, 0.5], **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Tutorial_Sample_Swatch.png')
    spd = colour.SpectralPowerDistribution(sample_spd_data)
    cmfs = colour.STANDARD_OBSERVERS_CMFS[
        'CIE 1931 2 Degree Standard Observer']
    illuminant = colour.ILLUMINANTS_SPDS['D65']
    with domain_range_scale('1'):
        XYZ = colour.spectral_to_XYZ(spd, cmfs, illuminant)
        RGB = colour.XYZ_to_sRGB(XYZ)
    plot_single_colour_swatch(
        ColourSwatch('Sample', RGB),
        text_parameters={'size': 'x-large'},
        **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Tutorial_Neutral5.png')
    patch_name = 'neutral 5 (.70 D)'
    patch_spd = colour.COLOURCHECKERS_SPDS['ColorChecker N Ohta'][patch_name]
    with domain_range_scale('1'):
        XYZ = colour.spectral_to_XYZ(patch_spd, cmfs, illuminant)
        RGB = colour.XYZ_to_sRGB(XYZ)
    plot_single_colour_swatch(
        ColourSwatch(patch_name.title(), RGB),
        text_parameters={'size': 'x-large'},
        **arguments)

    arguments['filename'] = os.path.join(output_directory,
                                         'Tutorial_Colour_Checker.png')
    plot_single_colour_checker(
        colour_checker='ColorChecker 2005',
        text_parameters={'visible': False},
        **arguments)

    arguments['filename'] = os.path.join(
        output_directory, 'Tutorial_CIE_1931_Chromaticity_Diagram.png')
    xy = colour.XYZ_to_xy(XYZ)
    plot_chromaticity_diagram_CIE1931(standalone=False)
    x, y = xy
    plt.plot(x, y, 'o-', color='white')
    # Annotating the plot.
    plt.annotate(
        patch_spd.name.title(),
        xy=xy,
        xytext=(-50, 30),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))
    render(
        standalone=True,
        limits=(-0.1, 0.9, -0.1, 0.9),
        x_tighten=True,
        y_tighten=True,
        **arguments)

    # *************************************************************************
    # "basics.rst"
    # *************************************************************************
    arguments['filename'] = os.path.join(output_directory,
                                         'Basics_Logo_Small_001_CIE_XYZ.png')
    RGB = colour.read_image(
        os.path.join(output_directory, 'Logo_Small_001.png'))[..., 0:3]
    XYZ = colour.sRGB_to_XYZ(RGB)
    colour.plotting.plot_image(
        XYZ, text_parameters={'text': 'sRGB to XYZ'}, **arguments)


if __name__ == '__main__':
    generate_documentation_plots(os.path.join('..', 'docs', '_static'))
