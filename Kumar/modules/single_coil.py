
import femm
import femm_sim.models.femm_model as femm_model
import femm_sim.models.coil as coil

femm.openfemm()   # The package must be initialized with the openfemm command.
femm.newdocument(0)   # We need to create a new Magnetostatics document to work on.

femm.mi_probdef(10000, 'millimeters', 'axi', 1.0e-10)
length = coil.Length(inn_layers=6, inn_rad=11, inn_wiredia=0.2032, inn_wireins=0.0178, innwind_pr_layer=100.5)
print('inn: ', length.inncoil())
inncoil_str = femm_model.Femm_coil(x1=11, y1=24, x2=11+(6*0.239), y2=0, circ_name='c2',
                                   circ_current=0.02, circ_type=1, material='32 AWG', edit_mode=4, group=1, label1=0.0178,
                                           label2=24, blockname='32 AWG', turns_pr_layer=100.5)
# magnetstr = femm_model.Femm_magnet(x1=0, y1=40, x2=5, y2=0,
#                                    material='N40', edit_mode=4, group=2, label1=0.5, label2=20)
bc = femm_model.Femm_bc(AirSpaceRadius_1=100, AirSpaceRadius_2=300, BC_Name='Outside', BC_Group=10, material='Air')
c1 = femm_model.Load_coil('c2')
a1 = c1.simulate()
print(a1)

#move_group = femm_model.Femm_move(groups = [1], x_dist=0, y_dist=1)
