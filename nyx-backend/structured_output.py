import json

def parse_structured_response(memorable_input):
  return_dict = {}
  if memorable_input.self_insights != "":
    return_dict["self_insights"] = memorable_input.self_insights
  if memorable_input.companion_insights != "":
    return_dict["companion_insights"] = memorable_input.companion_insights

    return return_dict
