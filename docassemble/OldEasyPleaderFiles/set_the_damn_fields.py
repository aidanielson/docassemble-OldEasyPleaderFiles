__all__ = ['set_docx_fields']

def set_docx_fields():
  propounder_docx_field = discov.propounder_list.true_values() if same_PP_and_RP else objection_categories[i].propounder_list.true_values()
  
  responder_docx_field = discov.responder_list.true_values() if same_PP_and_RP else objection_categories[i].responder_list.true_values()
  
  disco_svc_date_docx_field = discov.propound_svc_date_same_day if discov.propounded_same_day else objection_categories[i].date_disco_served
  
  disco_svc_method_docx_field = discov.svc_method_same_way if discov.served_same_way else objection_categories[i].disco_svc_method
  
  responses_svc_date_docx_field = discov.responses_svc_date_same_day if discov.responses_served_same_day else objection_categories[i].date_disco_served
  
  responses_svc_method_docx_field = discov.svc_method_same_way if discov.served_same_way else objection_categories[i].responses_svc_method