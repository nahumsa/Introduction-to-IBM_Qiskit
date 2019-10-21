from qiskit import IBMQ

def Print_status():
    """Print the status of each  IBM Q backend.
    This function was made originaly by 
    Leonardo Cirto.
    
    OUTPUT
    ---------------------------------
    NAME : 
    STATUS:
        backend_name    
        backend_version 
        status_msg      
        pending_jobs    
        operational     
    """
    provider = IBMQ.get_provider(group='open')
    backend_list = provider.backends()
    for BACKEND in backend_list:
        print(' NAME :', BACKEND)
        STATUS = BACKEND.status()
        print(' STATUS:' )
        print('    backend_name    =',  STATUS.backend_name )
        print('    backend_version =',  STATUS.backend_version )
        print('    status_msg      =',  STATUS.status_msg )
        print('    pending_jobs    =',  STATUS.pending_jobs )
        print('    operational     =',  STATUS.operational  )