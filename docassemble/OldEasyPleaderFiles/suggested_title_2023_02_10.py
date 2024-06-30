__all__ = ['set_sugg_doc_title']

def set_sugg_doc_title():
  if doc.sor == 'in support of':
    doc.title_suggested = f"{doc_type_for_title} {doc.sor} {client}'s {proceeding.moving_doc_title}"
  elif doc.sor == 'in opposition to':
    doc.title_suggested = f"{doc_type_for_title} {doc.sor} {proceeding.movant}'s {proceeding.moving_doc_title}"
  elif doc.sor == 'in reply to':
    doc.title_suggested = f"{doc_type_for_title} {doc.sor} {proceeding.opposer}'s opposition to {client}'s {proceeding.moving_doc_title}"
  else:
    doc.title_suggested = f"{doc_type_for_title} {doc.sor} {proceeding.movant}'s {proceeding.moving_doc_title}"
  return doc.title_suggested