# Copyright (C) 2020  Ssohrab Borhanian
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import numpy as np

from gwbench.utils import time_fac, REarth, halfTEarth, cLight, is_subset_lists, log_msg

cos = np.cos
sin = np.sin
exp = np.exp

ap_symbs_string = 'f Mc tc ra dec psi gmst0'

def detector_response(f, hfp, hfc, Mc, tc, ra, dec, psi, gmst0, loc, use_rot, user_locs=None):
    # input:    f       frequency domain [Hz]
    #           hfc     cross polarization
    #           hfp     plus polarization
    #           Mc      chirp Mass [solar mass]
    #           tc      time of coalescence [s]
    #           dec     declination [rad]
    #           ra      right ascencsion [rad]
    #           psi     polarization angle [rad]
    #           gmst0   GreenwichMeanSiderialTime according to LAL
    #           loc     location (and implied orientation) of a detector
    #           use_rot use frequency dependent time due to rotation of earth and SPA
    #
    # output:   hf      detector strain

    Fp, Fc, Flp = antenna_pattern_and_loc_phase_fac(f, Mc, tc, ra, dec, psi, gmst0, loc, use_rot, user_locs=user_locs)
    return Flp * (Fp * hfp + Fc * hfc)

def antenna_pattern_and_loc_phase_fac(f, Mc, tc, ra, dec, psi, gmst0, loc, use_rot, user_locs=None):
    # input:    f       frequency domain [Hz]
    #           Mc      chirp Mass [solar mass]
    #           tc      time of coalescence [s]
    #           dec     declination [rad]
    #           ra      right ascencsion [rad]
    #           psi     polarization angle [rad]
    #           gmst0   GreenwichMeanSiderialTime according to LAL
    #           loc     location (and implied orientation) of a detector
    #           use_rot use frequency dependent time due to rotation of earth and SPA
    #
    # output:   Fp, Fc, Flp

    gra  = calc_gra(ra, gmst0, use_rot, f, Mc, tc)
    D, d = det_ten_and_loc_vec(loc, REarth, user_locs=user_locs)

    return *ant_pat_funcs(D, *ant_pat_vectors(gra, dec, psi)), loc_phase_func(gra, dec, f, d)

def calc_gra(ra, gmst0, use_rot, f, Mc, tc):
    if use_rot is not None and use_rot: return gmst0 - ra + np.pi / halfTEarth * (tc - 5. / 256 * (time_fac * Mc)**(-5./3) * (np.pi * f)**(-8./3))
    else:                               return np.array([gmst0 - ra])

def loc_phase_func(gra, dec, f, d):
    theta = np.pi/2 - dec
    return exp(1j * 2 * np.pi * f * np.matmul(d, np.array([cos(gra)*sin(theta), sin(gra)*sin(theta), cos(theta)*np.ones_like(gra)])))

def ant_pat_funcs(D, XX, YY):
    return (0.5 * (np.matmul(D,XX) * XX - np.matmul(D,YY) * YY)).sum(axis=0), \
           (0.5 * (np.matmul(D,XX) * YY + np.matmul(D,YY) * XX)).sum(axis=0)

def ant_pat_vectors(gra, dec, psi):
    return np.array([ -cos(psi)*sin(gra) - sin(psi)*cos(gra)*sin(dec),
                      -cos(psi)*cos(gra) + sin(psi)*sin(gra)*sin(dec),
                                np.ones_like(gra) * sin(psi)*cos(dec) ]), \
           np.array([  sin(psi)*sin(gra) - cos(psi)*cos(gra)*sin(dec),
                       sin(psi)*cos(gra) + cos(psi)*sin(gra)*sin(dec),
                                np.ones_like(gra) * cos(psi)*cos(dec) ])

def det_ten_and_loc_vec(loc, R, user_locs=None):
    i_vec = np.array((1,0,0))
    j_vec = np.array((0,1,0))
    k_vec = np.array((0,0,1))

    et_vec2 = ( i_vec + np.sqrt(3.)*j_vec)/2.
    et_vec3 = (-i_vec + np.sqrt(3.)*j_vec)/2.

    alpha, beta, gamma, shape = det_angles_shape(loc, user_locs=user_locs)
    beta = np.pi/2 - beta
    EulerD1 = np.matmul(np.matmul(rot_mat(alpha,'k'), rot_mat(beta,'j')), rot_mat(gamma,'k'))

    if   shape == 'V3':
        eDArm1 = -1 * np.matmul(EulerD1,et_vec2)
        eDArm2 = -1 * np.matmul(EulerD1,et_vec3)
    elif shape == 'V2':
        eDArm1 =      np.matmul(EulerD1,et_vec3)
        eDArm2 = -1 * np.matmul(EulerD1,i_vec)
    elif shape == 'V1':
        eDArm1 =      np.matmul(EulerD1,i_vec)
        eDArm2 =      np.matmul(EulerD1,et_vec2)
    elif shape == 'L':
        eDArm1 =      np.matmul(EulerD1,i_vec)
        eDArm2 =      np.matmul(EulerD1,j_vec)

    return np.outer(eDArm1,eDArm1) - np.outer(eDArm2,eDArm2), R/cLight * np.matmul(EulerD1,k_vec)

def rot_mat(angle, axis):
    c = np.cos(angle)
    s = np.sin(angle)

    if axis == 'i': return np.array( ( (1,0,0), (0,c,-s), (0,s,c) ) )
    if axis == 'j': return np.array( ( (c,0,s), (0,1,0), (-s,0,c) ) )
    if axis == 'k': return np.array( ( (c,-s,0), (s,c,0), (0,0,1) ) )

def correct_arm_azimuth(arm_azimuth, which_arm):
    if   which_arm == 'x':        return np.pi/2 + arm_azimuth
    elif which_arm == 'y':        return           arm_azimuth
    elif which_arm == 'bisector': return np.pi/4 + arm_azimuth
    else: sys.exit('Unknown interferometer arm, specify which_arm as: "x", "y", or "bisect"!')

def det_angles_shape(loc, user_locs=None):
    # return alpha, beta, gamma in radians and shape of interferometer (e.g. 'L', 'V1', ...)
    # alpha ... longitude
    # beta  ... latitude
    # gamma ... angle from 'Due East' to y-arm
    # Switched to more precise angles for H, L, V, K, I, ET1, ET2, ET3 on 2022_03_29, found at:
    # https://lscsoft.docs.ligo.org/lalsuite/lal/_l_a_l_detectors_8h_source.html
    if user_locs is not None and loc in user_locs:
        user_loc = user_locs[loc]
        return user_loc['longitude'], user_loc['latitude'], correct_arm_azimuth(user_loc['arm_azimuth'], user_loc['which_arm']), user_loc['shape']
    # 2G sites
    elif loc == 'H':     return -2.08405676917,  0.81079526383, correct_arm_azimuth(np.pi-5.65487724844, 'y'), 'L'
    elif loc == 'L':     return -1.58430937078,  0.53342313506, correct_arm_azimuth(np.pi-4.40317772346, 'y'), 'L'
    elif loc == 'V':     return  0.18333805213,  0.76151183984, correct_arm_azimuth(np.pi-0.33916285222, 'y'), 'L'
    elif loc == 'K':     return  2.396441015,    0.6355068497,  correct_arm_azimuth(np.pi-1.054113,      'y'), 'L'
    elif loc == 'I':     return  1.33401332494,  0.24841853020, correct_arm_azimuth(np.pi-1.57079637051, 'y'), 'L'
    elif loc == 'LHO':   return -2.06982474503,  0.81079270401, correct_arm_azimuth(2.19910516123923,    'x'), 'L'
    elif loc == 'LLO':   return -1.5572845695,   0.53342110078, correct_arm_azimuth(3.45080197126464,    'x'), 'L'
    elif loc == 'LIO':   return  1.3444416672,   0.34231239582, correct_arm_azimuth(2.05248780779809,    'x'), 'L'
    # fiducial ET sites
    elif loc == 'ET1':   return  0.18333805213,  0.76151183984, correct_arm_azimuth(np.pi-0.33916285222, 'y'), 'V1'
    elif loc == 'ET2':   return  0.18333805213,  0.76151183984, correct_arm_azimuth(np.pi-0.33916285222, 'y'), 'V2'
    elif loc == 'ET3':   return  0.18333805213,  0.76151183984, correct_arm_azimuth(np.pi-0.33916285222, 'y'), 'V3'
    elif loc == 'ETS1':  return  0.1643518379,   0.70714923527, correct_arm_azimuth(1.5707963267949,     'x'), 'V1'
    elif loc == 'ETS2':  return  0.1643518379,   0.70714923527, correct_arm_azimuth(1.5707963267949,     'x'), 'V2'
    elif loc == 'ETS3':  return  0.1643518379,   0.70714923527, correct_arm_azimuth(1.5707963267949,     'x'), 'V3'
    # fiducial CE sites
    elif loc == 'C':     return -1.9691740,      0.764918,      correct_arm_azimuth(0.,                  'y'), 'L'
    elif loc == 'N':     return -1.8584265,      0.578751,      correct_arm_azimuth(-np.pi/3.,           'y'), 'L'
    elif loc == 'S':     return  2.5307270,     -0.593412,      correct_arm_azimuth(np.pi/4.,            'y'), 'L'
    elif loc == 'CEA':   return -2.18166156499,  0.80285145592, correct_arm_azimuth(4.53785605518526,    'x'), 'L'
    elif loc == 'CEB':   return -1.64060949687,  0.50614548308, correct_arm_azimuth(3.49065850398866,    'x'), 'L'
    elif loc == 'CES':   return  2.5307270,     -0.593412,      correct_arm_azimuth(np.pi/4.,            'y'), 'L'
    else: log_msg(f'det_angles_shape: Provided location {loc} is neither among the implemented locations nor in provided user_locs.', level='ERROR')
