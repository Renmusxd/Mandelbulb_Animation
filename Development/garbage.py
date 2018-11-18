#put unused, but maybe useful functions here

    @jit
    def sphere(self,Cx,Cy,Cz):
        if (Cx**2 + Cy**2 + Cz**2 >= self.vmax):
            return(False)
        else:
            return(True)