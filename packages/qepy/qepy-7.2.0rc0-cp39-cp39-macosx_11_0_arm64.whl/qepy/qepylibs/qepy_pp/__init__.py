from __future__ import print_function, absolute_import, division
pname = 'libqepy_pp'
# control the output
import sys
from importlib import import_module
from qepy.core import Logger, env
class QEpyLib :
    def __init__(self, **kwargs):
        qepylib = import_module(pname)
        sys.modules[pname] = self
        self.qepylib = qepylib

    def __getattr__(self, attr):
        attr_value = getattr(self.qepylib, attr)
        if '__array__' not in attr :
            attr_value = Logger.stdout2file(attr_value, fileobj=env['STDOUT'])
        return attr_value
qepylib = QEpyLib()
import libqepy_pp
import f90wrap.runtime
import logging
import qepy_pp.fermi_proj_routines
import qepy_pp.grid_module
import qepy_pp.pp_module
import qepy_pp.fs
import qepy_pp.wannier
import qepy_pp.eps_writer

def do_elf(elf):
    """
    do_elf(elf)
    
    
    Defined at elf.fpp lines 13-188
    
    Parameters
    ----------
    elf : float array
    
    -----------------------------------------------------------------------
      calculation of the electron localization function;
         elf = 1/(1+d**2)
      where
         d = ( t(r) - t_von_Weizacker(r) ) / t_Thomas-Fermi(r)
      and
         t(r) = (hbar**2/2m) * \sum_{k,i} |grad psi_{k,i}|**2
    (kinetic energy density)
         t_von_Weizaecker(r) = (hbar**2/2m) * 0.25 * |grad rho(r)|**2/rho
    (non-interacting boson)
         t_Thomas-Fermi(r) = (hbar**2/2m) * 3/5 * (3*pi**2)**(2/3) * rho**(5/3)
    (free electron gas)
      see also http://en.wikipedia.org/wiki/Electron_localization_function
    """
    libqepy_pp.f90wrap_do_elf(elf=elf)

def do_rdg(rdg):
    """
    do_rdg(rdg)
    
    
    Defined at elf.fpp lines 191-223
    
    Parameters
    ----------
    rdg : float array
    
    -----------------------------------------------------------------------
      reduced density gradient
         rdg(r) = (1/2) (1/(3*pi**2))**(1/3) * |\nabla rho(r)|/rho(r)**(4/3)
    """
    libqepy_pp.f90wrap_do_rdg(rdg=rdg)

def do_sl2rho(sl2rho):
    """
    do_sl2rho(sl2rho)
    
    
    Defined at elf.fpp lines 226-273
    
    Parameters
    ----------
    sl2rho : float array
    
    -----------------------------------------------------------------------
      Computes sign(l2)*rho(r), where l2 is the second largest eigenvalue
      of the electron-density Hessian matrix
    """
    libqepy_pp.f90wrap_do_sl2rho(sl2rho=sl2rho)

def do_dori(dori):
    """
    do_dori(dori)
    
    
    Defined at elf.fpp lines 276-318
    
    Parameters
    ----------
    dori : float array
    
    -----------------------------------------------------------------------
     D. Yang & Q.Liu
     density overlap regions indicator（DOI: 10.1021/ct500490b）
     theta(r) = 4 * (laplacian(rho(r)) * grad(rho(r)) * rho(r)
                + | grad(rho(r)) |**2 * grad(rho(r)))
                / (| grad(rho(r)) |**2)**3
     DORI(r) = theta(r) / (1 + theta(r))
    """
    libqepy_pp.f90wrap_do_dori(dori=dori)

def local_dos(iflag, lsign, kpoint, kband, spin_component, emin, emax, dos):
    """
    local_dos(iflag, lsign, kpoint, kband, spin_component, emin, emax, dos)
    
    
    Defined at local_dos.fpp lines 15-425
    
    Parameters
    ----------
    iflag : int
    lsign : bool
    kpoint : int
    kband : int
    spin_component : int
    emin : float
    emax : float
    dos : float array
    
    --------------------------------------------------------------------
         iflag=0: calculates |psi|^2 for band "kband" at point "kpoint"
         iflag=1: calculates the local density of state at e_fermi
    (only for metals)
         iflag=2: calculates the local density of  electronic entropy
    (only for metals with fermi spreading)
         iflag=3: calculates the integral of local dos from "emin" to "emax"
    (emin, emax in Ry)
         iflag=4: calculates |psi|^2 for all kpoints/bands that have
                  energy between "emin" and "emax" (emin, emax in Ry)
                  and spin = spin_component
         lsign:   if true and k=gamma and iflag=0, write |psi|^2 * sign(psi)
         spin_component: for iflag=3 and LSDA calculations only
                         0 for up+down dos,  1 for up dos, 2 for down dos
    """
    libqepy_pp.f90wrap_local_dos(iflag=iflag, lsign=lsign, kpoint=kpoint, \
        kband=kband, spin_component=spin_component, emin=emin, emax=emax, dos=dos)

def local_dos_mag(spin_component, kpoint, kband, raux):
    """
    local_dos_mag(spin_component, kpoint, kband, raux)
    
    
    Defined at local_dos_mag.fpp lines 14-276
    
    Parameters
    ----------
    spin_component : int
    kpoint : int
    kband : int
    raux : float array
    
    ----------------------------------------------------------------------------
     ... compute the contribution of band "kband" at k-point "kpoint"
     ... to the noncolinear magnetization for the given "spin_component"
    """
    libqepy_pp.f90wrap_local_dos_mag(spin_component=spin_component, kpoint=kpoint, \
        kband=kband, raux=raux)

def average():
    """
    average()
    
    
    Defined at average.fpp lines 13-373
    
    
    -----------------------------------------------------------------------
          Compute planar and macroscopic averages of a quantity(e.g. charge)
          in real space on a 3D FFT mesh. The quantity is read from a file
          produced by "pp.x", or from multiple files as follows:
              Q(i,j,k) = \sum_n w_n q_n(i,j,k)
          where q_n is the quantity for file n, w_n is a user-supplied weight
          The planar average is defined as
             p(k) = \sum_{i=1}^{N_1} \sum_{j=1}^{N_2} Q(i,j,k) / (N_1 N_2)
          along direction 3, and the like for directions 1 and 2;
          N_1, N_2, N_3 are the three dimensions of the 3D FFT.
          Note that if Q is a charge density whose integral is Z_v:
             Z_v = \int p(z) dV = \sum_k p(k) \Omega/N_3
          where \Omega is the size of the unit cell(or supercell)
          The planar average is then interpolated on the specified number
          of points supplied in input and written to file "avg.dat"
          The macroscopic average is defined as
             m(z) = \int_z^{z+a} p(z) dz
          where a is the size of the window(supplied in input)
          Input variables
          nfile        the number of files contaning the desired quantities
                       All files must refer to the same physical system
     for each file:
          filename     the name of the n-th file
          weight       the weight w_n of the quantity read from n-th file
          .
          .
     end
          npt          the number of points for the final interpolation of
                       the planar and macroscopic averages, as written to file
                       If npt <= N_idir(see below) no interpolation is done,
                       the N_idir FFT points in direction idir are printed.
          idir         1,2 or 3. Planar average is done in the plane orthogonal
                       to direction "idir", as defined for the crystal cell
          awin         the size of the window for macroscopic average(a.u.)
     Format of output file avg.dat:
        x   p(x)   m(x)
     where
        x = coordinate(a.u) along direction idir
            x runs from 0 to the length of primitive vector idir
      p(x)= planar average, as defined above
      m(x)= macroscopic average, as defined above
    """
    libqepy_pp.f90wrap_average()

def band_interpolation():
    """
    band_interpolation()
    
    
    Defined at band_interpolation.fpp lines 17-172
    
    
    ----------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_band_interpolation()

def do_bands():
    """
    do_bands()
    
    
    Defined at bands.fpp lines 14-627
    
    
    -----------------------------------------------------------------------
     See files INPUT_BANDS.* in Doc/ directory for usage
    """
    libqepy_pp.f90wrap_do_bands()

def d3hess():
    """
    d3hess()
    
    
    Defined at d3hess.fpp lines 13-373
    
    
    ---------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_d3hess()

def do_dos():
    """
    do_dos()
    
    
    Defined at dos.fpp lines 14-238
    
    
    --------------------------------------------------------------------
     Calculates the Density of States(DOS),
     separated into up and down components for LSDA
     See files INPUT_DOS.* in Doc/ directory for usage
     IMPORTANT: since v.5 namelist name is &dos and no longer &inputpp
    """
    libqepy_pp.f90wrap_do_dos()

def epsilon():
    """
    epsilon()
    
    
    Defined at epsilon.fpp lines 183-356
    
    
    ------------------------------
     Compute the complex macroscopic dielectric function,
     at the RPA level, neglecting local field effects.
     Eps is computed both on the real or immaginary axis
     Authors:
         2006 Andrea Benassi, Andrea Ferretti, Carlo Cavazzoni: basic \
             implementation(partly taken from pw2gw.f90)
         2007 Andrea Benassi: intraband contribution, nspin=2
         2016    Tae-Yun Kim, Cheol-Hwan Park:                       bugs fixed
         2016 Tae-Yun Kim, Cheol-Hwan Park, Andrea Ferretti: non-collinear magnetism \
             implemented
                                                                     code significantly restructured
    """
    libqepy_pp.f90wrap_epsilon()

def eps_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, nspin):
    """
    eps_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, nspin)
    
    
    Defined at epsilon.fpp lines 359-560
    
    Parameters
    ----------
    intersmear : float
    intrasmear : float
    nbndmin : int
    nbndmax : int
    shift : float
    metalcalc : bool
    nspin : int
    
    -----------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_eps_calc(intersmear=intersmear, intrasmear=intrasmear, \
        nbndmin=nbndmin, nbndmax=nbndmax, shift=shift, metalcalc=metalcalc, \
        nspin=nspin)

def jdos_calc(smeartype, intersmear, nbndmin, nbndmax, shift, nspin):
    """
    jdos_calc(smeartype, intersmear, nbndmin, nbndmax, shift, nspin)
    
    
    Defined at epsilon.fpp lines 563-825
    
    Parameters
    ----------
    smeartype : str
    intersmear : float
    nbndmin : int
    nbndmax : int
    shift : float
    nspin : int
    
    --------------------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_jdos_calc(smeartype=smeartype, intersmear=intersmear, \
        nbndmin=nbndmin, nbndmax=nbndmax, shift=shift, nspin=nspin)

def offdiag_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, \
    nspin):
    """
    offdiag_calc(intersmear, intrasmear, nbndmin, nbndmax, shift, metalcalc, nspin)
    
    
    Defined at epsilon.fpp lines 828-1017
    
    Parameters
    ----------
    intersmear : float
    intrasmear : float
    nbndmin : int
    nbndmax : int
    shift : float
    metalcalc : bool
    nspin : int
    
    -----------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_offdiag_calc(intersmear=intersmear, intrasmear=intrasmear, \
        nbndmin=nbndmin, nbndmax=nbndmax, shift=shift, metalcalc=metalcalc, \
        nspin=nspin)

def dipole_calc(ik, dipole_aux, metalcalc, nbndmin, nbndmax):
    """
    dipole_calc(ik, dipole_aux, metalcalc, nbndmin, nbndmax)
    
    
    Defined at epsilon.fpp lines 1020-1114
    
    Parameters
    ----------
    ik : int
    dipole_aux : complex array
    metalcalc : bool
    nbndmin : int
    nbndmax : int
    
    ------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_dipole_calc(ik=ik, dipole_aux=dipole_aux, \
        metalcalc=metalcalc, nbndmin=nbndmin, nbndmax=nbndmax)

def fermi_proj():
    """
    fermi_proj()
    
    
    Defined at fermi_proj.fpp lines 182-293
    
    
    ----------------------------------------------------------------------------
     Usage :
     $ proj_fermi.x -in {input file}
     Then it generates proj.frmsf(for nspin = 1, 4) or
     proj1.frmsf and proj2.frmsf(for nspin = 2)
     Input file format(projwfc.x + tail):
     &PROJWFC
     prefix = "..."
     outdir = "..."
     ...
     /
     {Number of target WFCs}
     {Index of WFC1} {Index of WFC2} {Index of WFC3} ...
    """
    libqepy_pp.f90wrap_fermi_proj()

def fermi_velocity():
    """
    fermi_velocity()
    
    
    Defined at fermi_velocity.fpp lines 20-155
    
    
    --------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fermi_velocity()

def fermisurface():
    """
    fermisurface()
    
    
    Defined at fermisurface.fpp lines 359-382
    
    
    --------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_fermisurface()

def initial_state():
    """
    initial_state()
    
    
    Defined at initial_state.fpp lines 13-89
    
    
    -----------------------------------------------------------------------
      compute initial-state contribution to core level shift
     input: namelist "&inputpp", with variables
       prefix      prefix of input files saved by program pwscf
       outdir      temporary directory where files resides
    """
    libqepy_pp.f90wrap_initial_state()

def molecularpdos():
    """
    molecularpdos()
    
    
    Defined at molecularpdos.fpp lines 13-416
    
    
    -----------------------------------------------------------------------
     Takes the projections onto orthogonalized atomic wavefunctions
     as computed by projwfc.x(see outdir/prefix.save/atomic_proj.xml)
     to build an LCAO-like representation of the eigenvalues of a system
     "full" and "part" of it(each should provide its own atomic_proj.xml file).
     Then the eigenvectors of the full system are projected onto the ones of the
     part.
     An explanation of the keywords and the implementation is provided in
     Scientific Reports | 6:24603 | DOI: 10.1038/srep24603(2016) (Supp. Info)
     Typical application: decompose the PDOS of an adsorbed molecule into
     its molecular orbital, as determined by a gas-phase calculation.
     The user has to specify which atomic functions(range beg:end) to use in
     both the full system and the part(the same atomic set should be used).
     MOPDOS(E,ibnd_part) = \sum_k w_k [ \sum_{ibnd_full}
                                        <psi_{ibnd_part,k}|psi_{ibnd_full,k}>
                                        * \delta(E-\epsilon_{ibnd_full,k}) *
                                        <psi_{ibnd_full,k}|psi_{ibnd_part,k}> ]
     where <psi_{ibnd_part,k}|psi_{ibnd_full,k}> are computed by using the LCAO
     representations:
     |psi_{ibnd_full,k}> =
            \sum_iatmwfc projs_full(iatmwfc,ibnd_full,k) |phi_{iatmwfc}>
     |psi_{ibnd_part,k}> =
            \sum_iatmwfc projs_part(iatmwfc,ibnd_part,k) |phi_{iatmwfc}>
     <psi_{ibnd_part,k}|psi_{ibnd_full,k}> =: projs_mo(ibnd_part,ibnd_full,k)
          = \sum_iatmwfc CONJG(projs_part(iatmwfc,ibnd_part,k))
                             * projs_full(iatmwfc,ibnd_full,k)
     If kresolveddos=.true. from input, the summation over k is not performed
     and individual k-resolved contributions are given in output.
    """
    libqepy_pp.f90wrap_molecularpdos()

def open_grid():
    """
    open_grid()
    
    
    Defined at open_grid.fpp lines 6-243
    
    
    ------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_open_grid()

def oscdft_et():
    """
    oscdft_et()
    
    
    Defined at oscdft_et.fpp lines 5-7
    
    
    """
    libqepy_pp.f90wrap_oscdft_et()

def oscdft_pp():
    """
    oscdft_pp()
    
    
    Defined at oscdft_pp.fpp lines 5-7
    
    
    """
    libqepy_pp.f90wrap_oscdft_pp()

def plan_avg():
    """
    plan_avg()
    
    
    Defined at plan_avg.fpp lines 14-283
    
    
    -----------------------------------------------------------------------
     calculate planar averages of each wavefunction
    """
    libqepy_pp.f90wrap_plan_avg()

def plotband():
    """
    plotband()
    
    
    Defined at plotband.fpp lines 12-785
    
    
    """
    libqepy_pp.f90wrap_plotband()

def plotproj():
    """
    plotproj()
    
    
    Defined at plotproj.fpp lines 12-150
    
    
    """
    libqepy_pp.f90wrap_plotproj()

def plotrho():
    """
    plotrho()
    
    
    Defined at plotrho.fpp lines 14-984
    
    
    -----------------------------------------------------------------------
       2D contour plot - logarithmically or linearly spaced levels
                       - Postscript printable output
       if " cplot" is called:
                       - contour lines plus gray levels
                       - negative values are shaded
       if "psplot" is called:
                       - contour lines of various kinds(solid, dashed, etc)
    """
    libqepy_pp.f90wrap_plotrho()

def pmw():
    """
    pmw()
    
    
    Defined at poormanwannier.fpp lines 14-392
    
    
    -----------------------------------------------------------------------
     projects wavefunctions onto atomic wavefunctions,
     input: namelist "&inputpp", with variables
       prefix      prefix of input files saved by program pwscf
       outdir      temporary directory where files resides
    """
    libqepy_pp.f90wrap_pmw()

def pp():
    """
    pp()
    
    
    Defined at postproc.fpp lines 257-293
    
    
    -----------------------------------------------------------------------
        Program for data analysis and plotting. The two basic steps are:
        1) read the output file produced by pw.x, extract and calculate
           the desired quantity(rho, V, ...)
        2) write the desired quantity to file in a suitable format for
           various types of plotting and various plotting programs
        The two steps can be performed independently. Intermediate data
        can be saved to file in step 1 and read from file in step 2.
        DESCRIPTION of the INPUT : see file Doc/INPUT_PP.*
    """
    libqepy_pp.f90wrap_pp()

def pprism():
    """
    pprism()
    
    
    Defined at postrism.fpp lines 15-115
    
    
    --------------------------------------------------------------------------
     ... Program to plot solvent distributions
     ... calculated by 3D-RISM or Laue-RISM
    """
    libqepy_pp.f90wrap_pprism()

def do_ppacf():
    """
    do_ppacf()
    
    
    Defined at ppacf.fpp lines 14-1229
    
    
    -----------------------------------------------------------------------
     This routine computes the coupling constant dependency of exchange
     correlation potential \( E_{\text{xc},\lambda}, \lambda \in \[0:1\]
     and the spatial distribution of exchange correlation energy
     density and kinetic correlation energy density according to:
     Y. Jiao, E. Schr\"oder, and P. Hyldgaard, Phys. Rev. B 97, 085115(2018).
     For an illustration of how to use this routine to set hybrid
     mixing parameter, please refer to:
     Y. Jiao, E. Schr\"oder, and P. Hyldgaard, J. Chem. Phys. 148, 194115(2018).
     Finally, this routine can also be used to set isolate the
      Ashcroft-type pure-dispersion component of E_{c;vdw}^nl
    (or the cumulant reminder, E_{c;alpha}^nl, defining a local-field \
        susceptibility):
     P. Hyldgaard, Y. Jiao, and V. Shukla, J. Phys.: Condens. Matt. 32, 393001(2020):
     https://iopscience.iop.org/article/10.1088/1361-648X/ab8250
    """
    libqepy_pp.f90wrap_do_ppacf()

def do_projwfc():
    """
    do_projwfc()
    
    
    Defined at projwfc.fpp lines 13-244
    
    
    -----------------------------------------------------------------------
     projects wavefunctions onto orthogonalized atomic wavefunctions,
     calculates Lowdin charges, spilling parameter, projected DOS
     or computes the LDOS in a volume given in input as function of energy
     See files INPUT_PROJWFC.* in Doc/ directory for usage
     IMPORTANT: since v.5 namelist name is &projwfc and no longer &inputpp
    """
    libqepy_pp.f90wrap_do_projwfc()

def get_et_from_gww(nbnd, et):
    """
    get_et_from_gww(nbnd, et)
    
    
    Defined at projwfc.fpp lines 246-280
    
    Parameters
    ----------
    nbnd : int
    et : float array
    
    """
    libqepy_pp.f90wrap_get_et_from_gww(nbnd=nbnd, et=et)

def print_lowdin(unit, nat, lmax_wfc, nspin, diag_basis, charges, \
    charges_lm=None):
    """
    print_lowdin(unit, nat, lmax_wfc, nspin, diag_basis, charges[, charges_lm])
    
    
    Defined at projwfc.fpp lines 283-377
    
    Parameters
    ----------
    unit : int
    nat : int
    lmax_wfc : int
    nspin : int
    diag_basis : bool
    charges : float array
    charges_lm : float array
    
    """
    libqepy_pp.f90wrap_print_lowdin(unit=unit, nat=nat, lmax_wfc=lmax_wfc, \
        nspin=nspin, diag_basis=diag_basis, charges=charges, charges_lm=charges_lm)

def sym_proj_g(rproj0, proj_out):
    """
    sym_proj_g(rproj0, proj_out)
    
    
    Defined at projwfc.fpp lines 381-452
    
    Parameters
    ----------
    rproj0 : float array
    proj_out : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_proj_g(rproj0=rproj0, proj_out=proj_out)

def sym_proj_k(proj0, proj_out):
    """
    sym_proj_k(proj0, proj_out)
    
    
    Defined at projwfc.fpp lines 456-527
    
    Parameters
    ----------
    proj0 : complex array
    proj_out : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_proj_k(proj0=proj0, proj_out=proj_out)

def sym_proj_so(domag, proj0, proj_out):
    """
    sym_proj_so(domag, proj0, proj_out)
    
    
    Defined at projwfc.fpp lines 531-633
    
    Parameters
    ----------
    domag : bool
    proj0 : complex array
    proj_out : float array
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_sym_proj_so(domag=domag, proj0=proj0, proj_out=proj_out)

def sym_proj_nc(proj0, proj_out):
    """
    sym_proj_nc(proj0, proj_out)
    
    
    Defined at projwfc.fpp lines 636-721
    
    Parameters
    ----------
    proj0 : complex array
    proj_out : float array
    
    """
    libqepy_pp.f90wrap_sym_proj_nc(proj0=proj0, proj_out=proj_out)

def print_proj(lmax_wfc, proj, lowdin_unit, diag_basis):
    """
    print_proj(lmax_wfc, proj, lowdin_unit, diag_basis)
    
    
    Defined at projwfc.fpp lines 724-882
    
    Parameters
    ----------
    lmax_wfc : int
    proj : float array
    lowdin_unit : int
    diag_basis : bool
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_print_proj(lmax_wfc=lmax_wfc, proj=proj, \
        lowdin_unit=lowdin_unit, diag_basis=diag_basis)

def force_theorem(ef_0, filproj):
    """
    force_theorem(ef_0, filproj)
    
    
    Defined at projwfc.fpp lines 885-981
    
    Parameters
    ----------
    ef_0 : float
    filproj : str
    
    """
    libqepy_pp.f90wrap_force_theorem(ef_0=ef_0, filproj=filproj)

def projwave_paw():
    """
    projwave_paw()
    
    
    Defined at projwfc.fpp lines 985-1078
    
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_projwave_paw()

def compute_mj(j, l, m):
    """
    compute_mj = compute_mj(j, l, m)
    
    
    Defined at projwfc.fpp lines 1082-1096
    
    Parameters
    ----------
    j : float
    l : int
    m : int
    
    Returns
    -------
    compute_mj : float
    
    -----------------------------------------------------------------------
    """
    compute_mj = libqepy_pp.f90wrap_compute_mj(j=j, l=l, m=m)
    return compute_mj

def projwave(filproj, filowdin, lsym, diag_basis, lwrite_ovp):
    """
    projwave(filproj, filowdin, lsym, diag_basis, lwrite_ovp)
    
    
    Defined at projwfc.fpp lines 1103-1729
    
    Parameters
    ----------
    filproj : str
    filowdin : str
    lsym : bool
    diag_basis : bool
    lwrite_ovp : bool
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_projwave(filproj=filproj, filowdin=filowdin, lsym=lsym, \
        diag_basis=diag_basis, lwrite_ovp=lwrite_ovp)

def rotate_basis(iuwfc):
    """
    lrotated = rotate_basis(iuwfc)
    
    
    Defined at projwfc.fpp lines 1732-2090
    
    Parameters
    ----------
    iuwfc : int
    
    Returns
    -------
    lrotated : bool
    
    """
    lrotated = libqepy_pp.f90wrap_rotate_basis(iuwfc=iuwfc)
    return lrotated

def pw2bgw():
    """
    pw2bgw()
    
    
    Defined at pw2bgw.fpp lines 117-4504
    
    
    -------------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_pw2bgw()

def pw2critic():
    """
    pw2critic()
    
    
    Defined at pw2critic.fpp lines 37-148
    
    
    """
    libqepy_pp.f90wrap_pw2critic()

def pw2gw():
    """
    pw2gw()
    
    
    Defined at pw2gw.fpp lines 26-1096
    
    
    -----------------------------------------------------------------------
     This subroutine writes files containing plane wave coefficients
     and other stuff needed by GW codes
    """
    libqepy_pp.f90wrap_pw2gw()

def pw2wannier90():
    """
    pw2wannier90()
    
    
    Defined at pw2wannier90.fpp lines 100-5184
    
    
    ------------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_pw2wannier90()

def sumpdos():
    """
    sumpdos()
    
    
    Defined at sumpdos.fpp lines 13-305
    
    
    """
    libqepy_pp.f90wrap_sumpdos()

def wannier_ham():
    """
    wannier_ham()
    
    
    Defined at wannier_ham.fpp lines 12-308
    
    
    -----------------------------------------------------------------------
     This program generates Hamiltonian matrix on Wannier-functions basis
    """
    libqepy_pp.f90wrap_wannier_ham()

def wannier_plot():
    """
    wannier_plot()
    
    
    Defined at wannier_plot.fpp lines 12-227
    
    
    -----------------------------------------------------------------------
     This program plots charge density of selected wannier function in
     IBM Data Explorer format
    """
    libqepy_pp.f90wrap_wannier_plot()

def wfck2r():
    """
    wfck2r()
    
    
    Defined at wfck2r.fpp lines 39-236
    
    
    -----------------------------------------------------------------------
    """
    libqepy_pp.f90wrap_wfck2r()


fermi_proj_routines = qepy_pp.fermi_proj_routines
grid_module = qepy_pp.grid_module
pp_module = qepy_pp.pp_module
fs = qepy_pp.fs
wannier = qepy_pp.wannier
eps_writer = qepy_pp.eps_writer
