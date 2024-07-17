def chapters_to_list(chapters):
    return chapters.split("\n")

def applyXML(text):
    return f"<?xml version='1.0'?><root>{text}</root>"

def wrapXML(text, tag):
    return f"<tag>{text}</tag>"