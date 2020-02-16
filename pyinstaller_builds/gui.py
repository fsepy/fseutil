# -*- coding: utf-8 -*-


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")

    import fseutil
    from fseutil.gui.__main__ import main

    print(f'FSEUTIL {fseutil.__version__}')
    print('THIS WINDOW IS ONLY VISIBLE IN DEV MODE.\n')
    
    main()
