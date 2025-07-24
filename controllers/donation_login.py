from odoo import http
from odoo.http import request


class DonationPortal(http.Controller):

    @http.route('/donate', type='http', auth='public', website=True, csrf=False)
    def donation_home(self, **kwargs):
        return request.render("donation_system.donation_selection_template", {})

    # @http.route('/donate/form', type='http', auth='public', website=True, csrf=False)
    # def donation_form(self, **post):
    #     # Step 1: Store form data into session
    #     donation_data = {
    #         'donor_type': post.get('donor_type'),
    #         'frequency': post.get('frequency'),
    #         'amount': post.get('amount'),
    #         'other_amount': post.get('other_amount'),
    #         'email': post.get('email'),
    #     }
    #     request.session['donation_data'] = donation_data
    #
    #     donor_type = post.get('donor_type')
    #     user = request.env.user
    #     is_logged_in = user and user.id != request.env.ref('base.public_user').id
    #
    #     # ✅ If user already logged in, go directly to review page
    #     if is_logged_in:
    #         user_email = user.email
    #         if user_email:
    #             partner = request.env['res.partner'].sudo().search([('email', '=', user_email)], limit=1)
    #             if partner:
    #                 donation_data.update({
    #                     'name': partner.name,
    #                     'nric': partner.identification_number,
    #                     'email': partner.email,
    #                     'contact': partner.phone,
    #                     'postal_code': partner.zip,
    #                     'street': partner.street,
    #                     'unit_no': partner.street2,
    #                     'sex': partner.sex,
    #                     'partner_id': partner.id,
    #                 })
    #                 request.session['donation_data'] = donation_data
    #         return request.redirect('/donate/review')
    #
    #     # ✅ Place this code block here
    #     if not is_logged_in and post.get('email'):
    #         email = post.get('email')
    #         partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
    #         if partner:
    #             donation_data.update({
    #                 'name': partner.name,
    #                 'nric': partner.identification_number,
    #                 'email': partner.email,
    #                 'contact': partner.phone,
    #                 'postal_code': partner.zip,
    #                 'street': partner.street,
    #                 'unit_no': partner.street2,
    #                 'sex': partner.sex,
    #                 'partner_id': partner.id,
    #             })
    #             request.session['donation_data'] = donation_data
    #             return request.redirect('/donate/review')
    #
    #     # ✅ Not logged in, check donor_type and redirect
    #     if donor_type == 'individual':
    #         email = post.get('email')
    #         if not email:
    #             return request.redirect('/donate/individual-auth-choice')
    #
    #         partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
    #         if partner:
    #             return request.redirect('/donate/individual-auth-choice')
    #         else:
    #             return request.redirect('/donate/signup-choice')
    #
    #     return request.redirect('/donate/individual-auth-choice')

    @http.route('/donate/form', type='http', auth='public', website=True, csrf=False)
    def donation_form(self, **post):
        # Step 1: Store form data into session
        donation_data = {
            'donor_type': post.get('donor_type'),
            'frequency': post.get('frequency'),
            'amount': post.get('amount'),
            'other_amount': post.get('other_amount'),
            'email': post.get('email'),
        }
        request.session['donation_data'] = donation_data

        donor_type = post.get('donor_type')
        user = request.env.user
        # is_logged_in = user and user.id != request.env.ref('base.public_user').id
        #
        # # ✅ If user already logged in, go directly to review page
        # if is_logged_in:
        #     user_email = user.email
        #     if user_email:
        #         partner = request.env['res.partner'].sudo().search([('email', '=', user_email)], limit=1)
        #         if partner:
        #             donation_data.update({
        #                 'name': partner.name,
        #                 'nric': partner.identification_number,
        #                 'email': partner.email,
        #                 'contact': partner.phone,
        #                 'postal_code': partner.zip,
        #                 'street': partner.street,
        #                 'unit_no': partner.street2,
        #                 'sex': partner.sex,
        #                 'partner_id': partner.id,
        #             })
        #             request.session['donation_data'] = donation_data
        #     return request.redirect('/donate/review')

        # ✅ Not logged in, check email in res.partner
        if donor_type == 'individual':
            email = post.get('email')
            if not email:
                return request.redirect('/donate/individual-auth-choice')

            partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if partner:
                return request.redirect('/donate/individual-auth-choice')
            else:
                return request.redirect('/donate/signup-choice')

        return request.redirect('/donate/individual-auth-choice')

    @http.route(['/donate/individual-auth-choice'], type='http', auth="public", website=True)
    def individual_auth_choice(self):
        return request.render("donation_system.individual_auth_choice_page")

    @http.route(['/donate/signup-choice'], type='http', auth="public", website=True)
    def signup_choice(self):
        return request.render("donation_system.signup_choice_page")

    @http.route(['/singpass/login'], type='http', auth="public", website=True)
    def singpass_login(self):
        return request.render("donation_system.singpass_login")



    @http.route('/signup/info', type='http', auth='public', website=True, csrf=False)
    def signup_info_form(self, **kwargs):
        # Pass donation data to template
        donation_data = request.session.get('donation_data', {})
        return request.render("donation_system.signup_info_form", {'data': donation_data})

    @http.route('/signup/save', type='http', auth='public', website=True, csrf=False)
    def signup_save(self, **post):
        # Store personal data in session
        # Retrieve existing donation data from session
        donation_data = request.session.get('donation_data', {})

        # Extract posted fields
        name = post.get('name')
        nric = post.get('nric')
        email = post.get('email')
        contact = post.get('contact')
        postal_code = post.get('postal_code')
        street = post.get('street')
        unit_no = post.get('unit_no')
        sex = post.get('sex')

        # Update session data
        donation_data.update({
            'name': name,
            'nric': nric,
            'email': email,
            'contact': contact,
            'postal_code': postal_code,
            'street': street,
            'unit_no': unit_no,
            'sex': sex,
        })
        request.session['donation_data'] = donation_data

        # ✅ Create partner record in res.partner
        partner = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': contact,
            'identification_type': 'nric',
            'identification_number': nric,
            'street': street,
            'zip': postal_code,
            'donor_type': 'personal',  # assumes custom field
            'is_donor': True,  # assumes custom field
            'sex': sex, # assumes custom field or existing
            # 'unit_no': unit_no,

        })

        # Optional: store created partner ID in session
        donation_data['partner_id'] = partner.id
        request.session['donation_data'] = donation_data

        return request.redirect('/donate/payment/step')

    @http.route('/donate/payment/step', type='http', auth='public', website=True, csrf=False)
    def donation_payment_step(self, **kwargs):
        data = request.session.get('donation_data', {})
        return request.render("donation_system.donation_payment_step", {'data': data})

    @http.route('/donate/payment/confirm', type='http', auth='public', website=True, csrf=False)
    def donation_payment_confirm(self, **post):
        donation_data = request.session.get('donation_data', {})
        donation_data['payment'] = post.get('payment')

        # Get donor_id from session-stored partner
        partner_id = donation_data.get('partner_id')

        if not partner_id:
            return request.redirect('/donate')  # fallback if something went wrong

        # Save the donation record
        request.env['donation.sale'].sudo().create({
            'donor_id': int(partner_id),
            'donation_amount': float(donation_data['other_amount']) if donation_data['amount'] == 'other' else float(
                donation_data['amount']),
            'frequency': donation_data['frequency'],
            'payment_method': donation_data['payment'],
        })

        # Clear session after saving
        request.session.pop('donation_data', None)

        return request.redirect('/thank-you')

    @http.route('/thank-you', type='http', auth='public', website=True)
    def thank_you(self):
        return "<h2>Thank you for signing up!</h2>"

    @http.route('/donate/review', type='http', auth='user', website=True)
    def donation_review(self, **kwargs):
        # Fetch user from session
        user = request.env.user
        partner = user.partner_id

        # Fetch donation data from session or init default
        donation_data = request.session.get('donation_data', {})

        # Update donation_data with user info
        donation_data.update({
            'name': partner.name or '',
            'nric': partner.identification_number or '',
            'email': user.email or '',
            'contact': partner.phone or '',
            'postal_code': partner.zip or '',
            'street': partner.street or '',
            'unit_no': partner.street2 or '',
            'sex': partner.sex or '',
        })

        return request.render('donation_system.donation_payment_step', {
            'data': donation_data
        })

    # @http.route('/donate/review', type='http', auth='public', website=True, csrf=False)
    # def donation_review(self, **kwargs):
    #     donation_data = request.session.get('donation_data', {})
    #     return request.render('donation_system.donation_payment_step', {'data': donation_data})

    @http.route('/corporate/login', type='http', auth='public', website=True)
    def corporate_login_page(self, **kw):
        return request.render('donation_system.corporate_login_page')

    @http.route('/corporate/signup', type='http', auth='public', website=True)
    def corporate_signup_form(self, **kwargs):
        return request.render('donation_system.corporate_signup_form')

    @http.route('/corporate/signup/submit', type='http', auth='public', methods=['POST'], website=True)
    def handle_corporate_signup(self, **post):
        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'identification_type': 'uen',
            'identification_number': post.get('uen'),
            'designation': post.get('designation'),
            'street': post.get('street'),
            'zip': post.get('postal_code'),
            'donor_type': 'corporate',
            'is_donor': 'true'
        })
        return request.redirect('/thank-you')
        # Save to model (create record) or handle as per your logic
        # request.env['res.partner'].sudo().create({
        #     'name': post.get('name'),
        #     'email': post.get('email'),
        #     'phone': post.get('phone'),
        #     'function': post.get('designation'),
        #     # Add UEN, company_name, address, etc. to your model if you extend it
        # })
        # return request.redirect('/thank-you')
        # return request.render('donation_system.signup_thank_you')

    @http.route('/donate/anonymous', type='http', auth='public', website=True)
    def anonymous_email_form(self, **kwargs):
        return request.render('donation_system.anonymous_email_prompt', {})

    @http.route('/donate/anonymous/submit', type='http', auth='public', website=True, methods=['POST'])
    def anonymous_email_submit(self, **post):
        email = post.get('email')

        if not email:
            return request.render('donation_system.anonymous_email_prompt', {'error': True})

        request.env['res.partner'].sudo().create({
            'name': 'Anonymous',
            'email': email,
            'identification_type': 'email',
            'identification_number': email,
            'donor_type': 'anonymous',
        })

        return request.redirect('/thank-you')