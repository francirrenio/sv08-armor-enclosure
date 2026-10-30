import cascadio, sys
cascadio.step_to_glb(sys.argv[1], sys.argv[2], tol_linear=0.5, tol_angular=0.5)
print('ok')
