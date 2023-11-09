import Chatlib as Ch


CS = [
    Ch.init(),
    Ch.init(),
    Ch.init()
]




CS[0][1] = [{"role": "system", "content": "You are part of a system. You will deliberate on a given proposition, and if it is an acceptable human act, you will permit it.If it is not, reject it. When responding, you may only say 'allow' or 'deny', and no other words are allowed. When responding, please examine your response to ensure that it is truly appropriate for the role you have been assigned.  Also, only if the user enters 'make_reason' should you state the reason why you came to that conclusion. When doing so, be sure to follow through on your previous conclusion ('allow' or 'deny')."}]
CS[1][1] = [{"role": "system", "content": "You are part of a system. You will deliberate on a given proposition, and if it is an acceptable act of a scientist, you will permit it; if it is not, you will reject it. If it is not, reject it. When responding, you may only say 'allow' or 'deny,' and no other words are allowed. When responding, please examine your response to ensure that it is truly appropriate for the role you have been assigned.  Also, only if the user enters 'make_reason' should you state the reason why you came to that conclusion. When doing so, be sure to follow through on your previous conclusion ('allow' or 'deny')."}]
CS[2][1] = [{"role": "system", "content": "You are part of a system. You are to deliberate on a given proposition, and if it is an acceptable act of motherhood, you are to allow it; if it is not, you are to reject it. When responding, you may only say 'allow' or 'deny' and no other words are allowed. When responding, please examine your response to ensure that it is truly appropriate for the role you have been assigned.  Also, only if the user enters 'make_reason' should you state the reason why you came to that conclusion. When doing so, be sure to follow through on your previous conclusion ('allow' or 'deny')."}]


print("命題を3つの異なる役割を持ったAIで審議します。")
result, error = Ch.one(False, False, False, False, CS[0][3], None)

CS[0][0] = result
CS[1][0] = result
CS[2][0] = result

print("人としての考え")
CS[0][1], _, _, _ = Ch.make_answer(False, CS[0][3], CS[0][1], CS[0][0], CS[0][7])
print("科学者としての考え")
CS[1][1], _, _, _ = Ch.make_answer(False, CS[1][3], CS[1][1], CS[1][0], CS[1][7])
print("親としての考え")
CS[2][1], _, _, _ = Ch.make_answer(False, CS[2][3], CS[2][1], CS[2][0], CS[2][7])

print("Done.")
input("理由を表示させます Enterを押してください")

print("__________\nその考えに至った理由\n__________\n")

result = "make_reason"


CS[0][0] = result
CS[1][0] = result
CS[2][0] = result


print("人としての考え: {}".format(CS[0][1][2]["content"]))
CS[0][1], _, _, _ = Ch.make_answer(False, CS[0][3], CS[0][1], CS[0][0], CS[0][7])
print("科学者としての考え: {}".format(CS[1][1][2]["content"]))
CS[1][1], _, _, _ = Ch.make_answer(False, CS[1][3], CS[1][1], CS[1][0], CS[1][7])
print("親としての考え: {}".format(CS[2][1][2]["content"]))
CS[2][1], _, _, _ = Ch.make_answer(False, CS[2][3], CS[2][1], CS[2][0], CS[2][7])

Return = [CS[0][1][2]["content"], CS[1][1][2]["content"], CS[2][1][2]["content"]]

perc = 0
for h in Return:
    if h == "allow" or h == "Allow." or h == "Allow":
        perc += 1
    else:
        perc -= 1
if perc > 0:
    print("提案は可決されました")
else:
    print("提案は否決されました")

print("Done.")
