import logging

from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from ..pydantic_models.user import UserIn

_logger = logging.getLogger(__name__)

class ContactService(Component):
    _inherit = 'base.rest.service'
    _name = 'contacts.service'
    _usage = 'contacts'
    _collection = 'photovoltaic_api.services'

    @restapi.method(
        [(['/'], 'POST')],
        # type=json,
        input_param=restapi.PydanticModel(UserIn),
        auth='api_key'
    )
    ### Will upsert contact based on email
    # 
    # 1. For "giver":
    # Create new entry if not exist
    # Update if existing
    #   - Adding notes
    # Warn if duplicated 
    
    # 2. For Receiver
    # - same story
    ###
    def create(self, contact_data):
    # def create(self, **contact_data):
        # contact_data = params
        _logger.info(f"contact__upsert : data : {contact_data}") # debug
        contact_dict = contact_data.dict(exclude_unset=True, exclude={'representative', 'interests', 'personal_data_policy', 'promotions', 'message_notes'})
        
        message_notes=contact_data.message_notes
        
        _logger.info(f"contact__upsert : dict : {contact_dict}") # debug
        _logger.info(f"message_notes : {message_notes}") # debug
        
        contact_mail = contact_dict['email']
        # contact_mail = params.get('email')
        _logger.info (f"mail: {contact_mail}")
        
        # Check if existing
        # contact_list = self.env['res.partner'].search({'email': contact_mail})
        contact_list = self.env['res.partner'].search([('email', '=', contact_mail)])
        # _logger.info (f"contact_list: {contact_list}") # debug
        
        created = False
        
        # mail not found
        if len(contact_list) == 0:
            _logger.info (f"[{contact_mail}] : not found : creating new entry")
            contact = self.env['res.partner'].create(contact_dict)
            created=True
            
        # mail exists
        else:
            
            # Pick first
            contact = contact_list[0]
            
            # More than one entry -> Add warning note
            if len(contact_list) > 1:
                warn_msg=f"[{contact_mail}] : {len(contact_list)} entries : {contact_list}"
                _logger.warn (warn_msg)
                contact.message_post(body=warn_msg) # TODO - Warning amarillo
                
            _logger.info (f"[{contact_mail}] : Updating existing entry [{contact.id}]")
            contact.write(contact_dict)
            
        
            
        # Add message notes
        if contact and message_notes:
            
            # Build message TODO remove ?
            # if contact['gift_from']:
                # message_body = f"Gift from {contact.gift_from} : {contact_data.amount}€ in {contact_data.plant}"
            # else: 
                # message_body = f"Gift from {contact['email']} : {contact_data['amount']} € in {contact_data['plant']}"
            
            
            # As it comes:
            message_body = message_notes
            # Store notes
            _logger.info (f"[{contact_mail}] : gift : adding message_body :\n{message_body}")
            contact.message_post(body=message_body)

            return {
                'result_upsert': 'created' if created else 'updated', # created/updated
                'message_body': message_body
            } # TODO algo mejor que enviar de vuelta?

        # return UserService._to_pydantic(self, contact) # esto falla porque se espera un objeto pydantic y no un dict, ademas le faltan campos

        return {
            'result_upsert': 'created' if created else 'updated', # created/updated
            'message_body': ''
        } # TODO algo mejor que enviar de vuelta?

