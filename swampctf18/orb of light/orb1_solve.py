encoded 		= "gh2AtAht hS zRfghLz ftg otozofE WRAtTz WhdAa gh2fAt hS gf9G AEEozAht Eftg WRfW zR9hogz EhfWRAtT EATRW lhotgf9Z hS Lh9Egz otGthLt Eftg hS zRfghLz, f WLAEATRW gh2fAt WRfW Az f gf9G 2A99h9, h9 ahiZ, hS ho9 Lh9Eg. f ihAtW hS lEATRW ftg ah99hzAht, f gh2fAt hoW hS zZta, f Eftg LAWR Rh99h9z 9ATRW lZ Zho ftg Zho ght'W GthL. f9WAzftz hS f WRfo2fWo9TAafE GAtg gh thW ozofEEZ a9hzz AtWh Eftgz hS zRfghL Sh9 At zoaR gh2fAtz ft otGthLt Rh99h9 Az zfAg Wh Eo9G. f99ArfE fELfZz l9AtTz flhoW gAzzhEoWAht hS fziA9fWAhtz Sh9 zRfghLz noAaGEZ zLfEEhL zhoEz hS EATRW At f 2ZzWAa A2ihzzAlAEAWZ. f zhEAWf9Z foTo9Z Lfz i9hhS: GAtTgh2z LAEE SfEE fz ahtNo9fWAht hS zRfghL TEhh2z 2AggfZ LAWR gf9G 2fEAaAhoz ShT, f Eo2Athoz aRf92 LAEE afzW f 9fZ WRfW fTfAt fEATtz ho9 Lh9Eg."
bad_plaintext 	= "do2InIon oF sHadoWs and unusuaL THInNs To?Ii do2aIn oF da9D ILLusIon Land THaT sH9ouds LoaTHInN LINHT wounda9S oF Wo9Lds unDnoWn Land oF sHadoWs, a TWILINHT do2aIn THaT Is a da9D 2I99o9, o9 io?S, oF ou9 Wo9Ld. a ?oInT oF wLINHT and io99osIon, a do2aIn ouT oF sSni, a Land WITH Ho99o9s 9INHT wS Sou and Sou don'T DnoW. a9TIsans oF a THau2aTu9NIiaL DInd do noT usuaLLS i9oss InTo Lands oF sHadoW Fo9 In suiH do2aIns an unDnoWn Ho99o9 Is saId To Lu9D. a99IhaL aLWaSs w9InNs awouT dIssoLuTIon oF as?I9aTIons Fo9 sHadoWs ?uIiDLS sWaLLoW souLs oF LINHT In a 2SsTIi I2?ossIwILITS. a soLITa9S auNu9S Was ?9ooF: DInNdo2s WILL FaLL as ion?u9aTIon oF sHadoW NLoo2s 2IddaS WITH da9D 2aLIiIous FoN, a Lu2Inous iHa92 WILL iasT a 9aS THaT aNaIn aLINns ou9 Wo9Ld."

cipher = {}
for i in range(len(encoded)):
  cipher[encoded[i]] = bad_plaintext[i].lower()

cipher['2'] = 'm'
cipher['T'] = 'g'
cipher['9'] = 'r'
cipher['G'] = 'k'
cipher['a'] = 'c'
cipher['Z'] = 'y'
cipher['n'] = 'q'
cipher['i'] = 'p'
cipher['l'] = 'b'
cipher['N'] = 'j'
cipher['d'] = 'x'
cipher['r'] = 'v'

cipher['{'] = 'e'
cipher['}'] = 'z'

plaintext = ""

for i in encoded:
  if i in cipher:
    plaintext += cipher[i]
  else:
    plaintext += i

cipher_output = sorted( ((v,k) for k,v in cipher.iteritems()), reverse=False)

flag = "" 
for i,j in cipher_output:
  flag += j
  
print flag