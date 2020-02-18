# -*- coding: utf-8 -*-
import datetime

if __name__ == "__main__":
    import os
    import warnings
    warnings.filterwarnings("ignore")

    import fseutil
    from fseutil.gui.__main__ import main

    print(os.path.realpath(__file__))
    print('='*80)
    print('FSEUTIL')
    print(f'VERSION: {fseutil.__version__}.')
    print(f'RELEASED: {fseutil.__date_released__.strftime("%Y %B %d")}.')
    _exp = fseutil.__date_released__ + datetime.timedelta(days=fseutil.__expiry_period_days__) - datetime.datetime.now()
    _exp_d, _ = divmod(_exp.total_seconds(), 24 * 60 * 60)
    _exp_h, _ = divmod(_, 60 * 60)
    _exp_m, _ = divmod(_, 60)
    print(f'EXPIRES IN: {_exp_d:.0f} day(s), {_exp_h:.0f} hour(s) and {_exp_m:.0f} minute(s).')
    print('(THIS WINDOW IS ONLY VISIBLE IN DEV MODE WHEN VERSION CONTAINS DEV KEYWORD.)')
    print('='*80)

    main()
