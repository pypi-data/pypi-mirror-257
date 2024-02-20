from __future__ import print_function, absolute_import, division
pname = 'libqepy_modules'
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
import libqepy_modules
import f90wrap.runtime
import logging
import qepy_modules.gvect
import qepy_modules.mp_bands_tddfpt
import qepy_modules.funct
import qepy_modules.ions_base
import qepy_modules.mp_bands
import qepy_modules.io_global
import qepy_modules.control_flags
import qepy_modules.cell_base
import qepy_modules.check_stop
import qepy_modules.command_line_options
import qepy_modules.mp_pools
import qepy_modules.read_input
import qepy_modules.mp_world
import qepy_modules.environment
import qepy_modules.mp_orthopools
import qepy_modules.qepy_sys
import qepy_modules.wavefunctions
import qepy_modules.constants
import qepy_modules.gvecs
import qepy_modules.mp_global
import qepy_modules.qexsd_module
import qepy_modules.open_close_input_file

def impose_deviatoric_strain(at_old, at):
    """
    impose_deviatoric_strain(at_old, at)
    
    
    Defined at deviatoric.fpp lines 14-34
    
    Parameters
    ----------
    at_old : float array
    at : float array
    
    ---------------------------------------------------------------------
     Impose a pure deviatoric(volume-conserving) deformation.
     Needed to enforce volume conservation in variable-cell MD/optimization.
    """
    libqepy_modules.f90wrap_impose_deviatoric_strain(at_old=at_old, at=at)

def impose_deviatoric_strain_2d(at_old, at):
    """
    impose_deviatoric_strain_2d(at_old, at)
    
    
    Defined at deviatoric.fpp lines 38-61
    
    Parameters
    ----------
    at_old : float array
    at : float array
    
    ---------------------------------------------------------------------
     Modification of \(\texttt{impose\_deviatoric\_strain}\) but for
     Area conserving deformation(2DSHAPE).
     Added by Richard Charles Andrew, Physics Department, University if Pretoria,
     South Africa, august 2012.
    """
    libqepy_modules.f90wrap_impose_deviatoric_strain_2d(at_old=at_old, at=at)

def impose_deviatoric_stress(sigma):
    """
    impose_deviatoric_stress(sigma)
    
    
    Defined at deviatoric.fpp lines 65-78
    
    Parameters
    ----------
    sigma : float array
    
    ---------------------------------------------------------------------
     Impose a pure deviatoric stress.
    """
    libqepy_modules.f90wrap_impose_deviatoric_stress(sigma=sigma)

def impose_deviatoric_stress_2d(sigma):
    """
    impose_deviatoric_stress_2d(sigma)
    
    
    Defined at deviatoric.fpp lines 82-96
    
    Parameters
    ----------
    sigma : float array
    
    ---------------------------------------------------------------------
     Modification of \(\texttt{impose_deviatoric_stress} but for
     Area conserving deformation(2DSHAPE).
     Added by Richard Charles Andrew, Physics Department, University if Pretoria,
     South Africa, august 2012
    """
    libqepy_modules.f90wrap_impose_deviatoric_stress_2d(sigma=sigma)

def set_para_diag(nbnd, use_para_diag):
    """
    set_para_diag(nbnd, use_para_diag)
    
    
    Defined at set_para_diag.fpp lines 13-61
    
    Parameters
    ----------
    nbnd : int
    use_para_diag : bool
    
    -----------------------------------------------------------------------------
     Sets up the communicator used for parallel diagonalization in LAXlib.
     Merges previous code executed at startup with function "check_para_diag".
     To be called after the initialization of variables is completed and
     the dimension of matrices to be diagonalized is known
    """
    libqepy_modules.f90wrap_set_para_diag(nbnd=nbnd, use_para_diag=use_para_diag)

def plugin_arguments():
    """
    plugin_arguments()
    
    
    Defined at plugin_arguments.fpp lines 13-74
    
    
    -----------------------------------------------------------------------------
     Check for presence of command-line option "-plugin\_name" or "--plugin_name"
     where "plugin\_name" has to be set here. If such option is found, variable
     \(\text{use_plugin_name}\) is set and usage of "plugin\_name" is thus enabled.
     Currently implemented: "plumed", "pw2casino" (both case-sensitive).
    """
    libqepy_modules.f90wrap_plugin_arguments()

def plugin_arguments_bcast(root, comm):
    """
    plugin_arguments_bcast(root, comm)
    
    
    Defined at plugin_arguments.fpp lines 78-107
    
    Parameters
    ----------
    root : int
    comm : int
    
    ----------------------------------------------------------------------------
     Broadcast plugin arguments.
    """
    libqepy_modules.f90wrap_plugin_arguments_bcast(root=root, comm=comm)


gvect = qepy_modules.gvect
mp_bands_tddfpt = qepy_modules.mp_bands_tddfpt
funct = qepy_modules.funct
ions_base = qepy_modules.ions_base
mp_bands = qepy_modules.mp_bands
io_global = qepy_modules.io_global
control_flags = qepy_modules.control_flags
cell_base = qepy_modules.cell_base
check_stop = qepy_modules.check_stop
command_line_options = qepy_modules.command_line_options
mp_pools = qepy_modules.mp_pools
read_input = qepy_modules.read_input
mp_world = qepy_modules.mp_world
environment = qepy_modules.environment
mp_orthopools = qepy_modules.mp_orthopools
qepy_sys = qepy_modules.qepy_sys
wavefunctions = qepy_modules.wavefunctions
constants = qepy_modules.constants
gvecs = qepy_modules.gvecs
mp_global = qepy_modules.mp_global
qexsd_module = qepy_modules.qexsd_module
open_close_input_file = qepy_modules.open_close_input_file
