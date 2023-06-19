from sfepy.terms.terms import Term, terms

class LinearVolumeForceTerm(Term):
    r"""
    Vector or scalar linear volume forces (weak form) --- a right-hand side
    source term.

    :Definition:

    .. math::
        \int_{\Omega} \ul{f} \cdot \ul{v} \mbox{ or } \int_{\Omega} f q

    :Arguments:
        - material : :math:`\ul{f}` or :math:`f`
        - virtual  : :math:`\ul{v}` or :math:`q`
    """
    name = 'dw_volume_lvf'
    arg_types = ('material', 'virtual')
    arg_shapes = [{'material' : 'D, 1', 'virtual' : ('D', None)},
                  {'material' : '1, 1', 'virtual' : (1, None)}]

    function = staticmethod(terms.dw_volume_lvf)

    def get_fargs(self, mat, virtual,
                  mode=None, term_mode=None, diff_var=None, **kwargs):
        vg, _ = self.get_mapping(virtual)

        return mat, vg


class NonLinearVolumeForceTerm(Term):
    """
     Product of virtual and function of state.

    :Definition:

    .. math::
        \int_{\Omega} q f(p)

    :Arguments 1:
        - function : :math:`f`
        - virtual  : :math:`q`
        - state    : :math:`p`

    """
    name = 'dw_volume_nvf'
    arg_types = ('fun', 'fun_d', 'virtual', 'state')
    arg_shapes = {'material_fun'        : '1: 1',
                   'material_fun_d'      : '1: 1',
                   'virtual'  : (1, 'state'),
                   'state'    : 1}
    

    @staticmethod
    def function(out, out_qp, geo, fmode):
        status = geo.integrate(out, out_qp)
        return status


    def get_fargs(self, fun, dfun, var1, var2,
                  mode=None, term_mode=None, diff_var=None, **kwargs):
        vg1, _ = self.get_mapping(var1)
        vg2, _ = self.get_mapping(var2)

        if diff_var is None:
            geo = vg1
            val_qp = fun(self.get(var2, 'val'))            
            out_qp = dot_sequences(vg1.bf, val_qp,'ATB')
            
            fmode = 0

        else:
            geo = vg1
            val_d_qp = dfun(self.get(var2, 'val'))
            out_qp = dot_sequences(vg1.bf, val_d_qp*vg2.bf,'ATB')
                
            fmode = 1

        return out_qp, geo, fmode
