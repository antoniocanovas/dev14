# -*- coding: utf-8 -*-
#imports of python lib
import logging
# imports of odoo lib
from odoo.http import request
# imports of odoo addons
from odoo.addons.web.controllers.main import Home as Home

_logger = logging.getLogger(__name__)


class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        # Login redirect directly to the session
        res_users_obj = request.env['res.users']
        if uid:
            _logger.info('**** Login Redirect****')
            search_user = res_users_obj.search([('id', '=', uid)], limit=1)
            if search_user and search_user.pos_config_id:
                _logger.info('****Redirect**** %s', redirect)
                _logger.info(search_user.pos_config_id.current_session_state)
                _logger.info(search_user.pos_config_id.pos_session_username)
                _logger.info(request.env.user.name)
                if search_user.pos_config_id.pos_session_state == False and search_user.pos_config_id.pos_session_username == False:
                    _logger.info('**** If****')
                    search_user.pos_config_id.open_session_cb()
                    if search_user.pos_config_id.cash_control:
                        search_user.pos_config_id.current_session_id.action_pos_session_open()
                    if redirect:
                        return redirect
                    else:
                        return '/pos/web?config_id='+str(search_user.pos_config_id.id)
                    #return redirect if redirect else '/pos/web'
                elif search_user.pos_config_id.current_session_state == 'opened' and search_user.pos_config_id.pos_session_username == request.env.user.name:
                    _logger.info('**** Else If****')
                    #===========================================================
                    # if redirect:
                    #     _logger.info('**** If****')
                    #     return redirect
                    # else:
                    #===========================================================
                    return '/pos/web?config_id='+str(search_user.pos_config_id.id)
                else:
                    _logger.info('**** Else****')
                    return redirect if redirect else '/web'
        return redirect if redirect else '/web'
