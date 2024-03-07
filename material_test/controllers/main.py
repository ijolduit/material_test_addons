from odoo import http
from odoo.http import request
import json
from datetime import datetime, timedelta
from pytz import timezone

APIKEY = '$2y$10$t7ZPJgiZBJWvH36ceZPU1ONij9F2Who0xl.632mRpQbMhTFAUHlNC'

class ApiMaterialController(http.Controller):
    def verification_access(self, request):
        success = "0"
        datas = []
        errors = []
        api_key = request.httprequest.headers.get('Api-key')
        if not api_key:
            success = "0"
            errors.append({"error": "Api key not found"})

        if request.httprequest.headers.get('Api-key'):

            key = request.httprequest.headers.get('Api-key')

            if key == APIKEY:
                # Check in partner data email or phone
                # Check for phone or email has been exist
                success = "1"
            else:
                success = "0"
                errors.append({"error": "Authentication failed"})

        result = {
            "success": success,
            "datas": datas,
            "errors": errors
        }
        return result

    def gen_result(self,success,datas,errors):
        result = {
            "success": success,
            "datas": datas,
            "errors": errors}
        return result

    @http.route('/api/v1/material/create', type='json', auth="public", csrf=False, methods=['POST'])
    def ApiMaterialCreate(self, values=None):
        success = "0"
        datas = []
        errors = []

        result = self.verification_access(request)
        if result.get('success') == "0":
            return result


        try:
            values = json.loads(request.httprequest.data)
            vals = {
                'name': values['name'],
                'code': values['code'],
                'type': values['type'],
                'buy_price': values['buy_price'],
                'related_supplier': values['related_supplier'],


            }
            request.env['test.material'].sudo().create(vals)

        except Exception as e:
            success = "0"
            errors.append({"error": str(e)})
            request.env.cr.rollback()


        result = {
            "success": success,
            "datas": datas,
            "errors": errors}
        return result

    @http.route('/api/v1/material/edit', type='json', auth="public", csrf=False, methods=['POST'])
    def ApiMaterialEdit(self, values=None):
        success = "0"
        datas = []
        errors = []

        result = self.verification_access(request)
        if result.get('success') == "0":
            return result

        try:
            values = json.loads(request.httprequest.data)
            # FIND MATERIAL BY CODE

            material_id = request.env['test.material'].sudo().search([('code','=',values['code'])],limit=1)
            if not material_id:
                success = "0"
                data = []
                errors.append({"error": "MATERIAL CODE NOT FOUND"})
                result = self.gen_result(success, data, errors)
                return result

            vals = {
                'name': values['name'],
                'code': values['code'],
                'type': values['type'],
                'buy_price': values['buy_price'],
                'related_supplier': values['related_supplier'],
            }

            material_id.sudo().write(vals)

        except Exception as e:
            success = "0"
            errors.append({"error": str(e)})
            request.env.cr.rollback()

        result = {
            "success": success,
            "datas": datas,
            "errors": errors}
        return result

    @http.route('/api/v1/material/delete', type='json', auth="public", csrf=False, methods=['POST'])
    def ApiMaterialDelete(self, values=None):
        success = "0"
        datas = []
        errors = []

        result = self.verification_access(request)
        if result.get('success') == "0":
            return result

        try:
            values = json.loads(request.httprequest.data)
            # FIND MATERIAL BY CODE

            material_id = request.env['test.material'].sudo().search([('code', '=', values['code'])], limit=1)
            if not material_id:
                success = "0"
                data = []
                errors.append({"error": "MATERIAL CODE NOT FOUND"})
                result = self.gen_result(success, data, errors)
                return result


            material_id.sudo().unlink()

        except Exception as e:
            success = "0"
            errors.append({"error": str(e)})
            request.env.cr.rollback()

        result = {
            "success": success,
            "datas": datas,
            "errors": errors}
        return result