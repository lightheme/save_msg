aiter = client.iter_dialogs(limit=30) if offset == 0 else aislice(client.iter_dialogs(limit=(offset + 1) * 30), 0,
                                                                   offset * 30)
