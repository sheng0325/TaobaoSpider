

# https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/


headers = {
  # cookie 用户信息，常用于检测是否有登入账号信息
  'cookie':'_samesite_flag_=true; cookie2=14daf532cae877f9975af5cf9f198782; t=ad776bf3433c2b95f94993d613cefbcb; _tb_token_=78bbe67073ea8; wk_cookie2=1cda2c827cc2086403dcd2467001f2cc; wk_unb=UUpgQyuEPYo8dWHcTg%3D%3D; thw=cn; useNativeIM=false; havana_lgc2_0=eyJoaWQiOjIyMTUyMDI4ODMyMzEsInNnIjoiZDZjNjk5ZTYwMWVmM2E1OGQzNGMzYTljMTQyM2QxYzUiLCJzaXRlIjowLCJ0b2tlbiI6IjFFRG1wTGVMOTFJTC04UUZ6OWxVNVRnIn0; _hvn_lgc_=0; sn=; lgc=tb840657587241; cancelledSubSites=empty; dnk=tb840657587241; tracknick=tb840657587241; cna=QSD0HThygTMCAXL2xCRlUDLD; hng=CN%7Czh-CN%7CCNY%7C156; mtop_partitioned_detect=1; _m_h5_tk=096a0eb6686d0d3353112ac13870954f_1737215781482; _m_h5_tk_enc=62e4f57219ebe2f10ee8fded5897a41d; _uetsid=52b94520d5a211efb74831dc5c336cf6; _uetvid=9c24c2c0924811eeb4b3b37641522e58; sgcookie=E100kdJ4xtcfHxa6BHlu6rn0%2FJka7QnAj%2F%2Ba1%2FLi2RlPlNQe27zWBmqheJuGXUlinRNQNalV5w7bgJubBXJwAhmB4OhR6JeBeXr2SZQfsTtIeNo%3D; havana_lgc_exp=1768311863191; unb=2215202883231; uc1=existShop=false&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0&cookie14=UoYdWtKMZnMyUQ%3D%3D&cookie21=URm48syIYn73&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D; uc3=id2=UUpgQyuEPYo8dWHcTg%3D%3D&vt3=F8dD37F9dR26J5N2WI8%3D&nk2=F5RNYQPYyWTEPWdB1Ro%3D&lg2=UIHiLt3xD8xYTw%3D%3D; csg=41ec2965; cookie17=UUpgQyuEPYo8dWHcTg%3D%3D; skt=44357d24ca3c6fa8; existShop=MTczNzIwNzg2Mw%3D%3D; uc4=nk4=0%40FY4GtgrWBNJP1PyjKFOQXFPGPpnlOsPcmg%3D%3D&id4=0%40U2gqzJ04nR8Ud43ElFw%2FUXVBkws3D9dS; _cc_=VT5L2FSpdA%3D%3D; _l_g_=Ug%3D%3D; sg=113; _nk_=tb840657587241; cookie1=UoLcq89gyrj7%2FTwf8hbDUv8CHDw5RReo%2Bt0%2FLBe9fU4%3D; sdkSilent=1737294263196; havana_sdkSilent=1737294263196; 3PcFlag=1737207880216; fastSlient=1737207880230; xlly_s=1; tfstk=gWkZgns8Q-0QT9nrRY2VUGGkoh2TF-8WQxabmmm0fP4g5mq0320XXPiDWqk4-mh6XSTO0GHEzt66WCnc3-wDPU9WFcITH-Y5ONGFqPExxrxQsNogBG2DPU9COMV95-0_L8qH86q8-lq0S1xUKor8nlXmoyV3qu_gnq2DYMquVZX0itbHKyE0nr00nHy3Jo8u25VckuVMm-JJEDCbf5zojyWqDvrg_1ng8tXmLXParTaFntDUjDNSLHXMUycsiAwnIeb8K0hISkyy3irEaD2gbqpRBRmoxjVZ3Is8kXonNWldfhEEQ0k44WQHbrHs7xPtEU6LSXkK3RGB7TaYiXMTwAThQ8c-fRGm-nX0uXqc4J_YxlmxHf7cg5qLYzteY8cZhByf6O9hMsFnykzWX75AM5VuYzteYsCY6OEUPhFP.; isg=BPb2Guv8jcoMfnvIog38B42NRyr4FzpRPy00F2Df4ll0o5Y9yKeKYVxVu3fPCzJp'
  #user-agent 用户代理，表示浏览器基本身份信息
  'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  
}

#请求网址
url = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?jsv=2.7.4&appKey=12574478&t=1737207989874&sign=6491bfdc7d49a96a541b67f3e3c4ee81&api=mtop.relationrecommend.wirelessrecommend.recommend&v=2.0&timeout=10000&type=jsonp&dataType=jsonp&callback=mtopjsonp5&data=%7B%22appId%22%3A%2234385%22%2C%22params%22%3A%22%7B%5C%22device%5C%22%3A%5C%22HMA-AL00%5C%22%2C%5C%22isBeta%5C%22%3A%5C%22false%5C%22%2C%5C%22grayHair%5C%22%3A%5C%22false%5C%22%2C%5C%22from%5C%22%3A%5C%22nt_history%5C%22%2C%5C%22brand%5C%22%3A%5C%22HUAWEI%5C%22%2C%5C%22info%5C%22%3A%5C%22wifi%5C%22%2C%5C%22index%5C%22%3A%5C%224%5C%22%2C%5C%22rainbow%5C%22%3A%5C%22%5C%22%2C%5C%22schemaType%5C%22%3A%5C%22auction%5C%22%2C%5C%22elderHome%5C%22%3A%5C%22false%5C%22%2C%5C%22isEnterSrpSearch%5C%22%3A%5C%22true%5C%22%2C%5C%22newSearch%5C%22%3A%5C%22false%5C%22%2C%5C%22network%5C%22%3A%5C%22wifi%5C%22%2C%5C%22subtype%5C%22%3A%5C%22%5C%22%2C%5C%22hasPreposeFilter%5C%22%3A%5C%22false%5C%22%2C%5C%22prepositionVersion%5C%22%3A%5C%22v2%5C%22%2C%5C%22client_os%5C%22%3A%5C%22Android%5C%22%2C%5C%22gpsEnabled%5C%22%3A%5C%22false%5C%22%2C%5C%22searchDoorFrom%5C%22%3A%5C%22srp%5C%22%2C%5C%22debug_rerankNewOpenCard%5C%22%3A%5C%22false%5C%22%2C%5C%22homePageVersion%5C%22%3A%5C%22v7%5C%22%2C%5C%22searchElderHomeOpen%5C%22%3A%5C%22false%5C%22%2C%5C%22search_action%5C%22%3A%5C%22initiative%5C%22%2C%5C%22sugg%5C%22%3A%5C%22_4_1%5C%22%2C%5C%22sversion%5C%22%3A%5C%2213.6%5C%22%2C%5C%22style%5C%22%3A%5C%22list%5C%22%2C%5C%22ttid%5C%22%3A%5C%22600000%40taobao_pc_10.7.0%5C%22%2C%5C%22needTabs%5C%22%3A%5C%22true%5C%22%2C%5C%22areaCode%5C%22%3A%5C%22CN%5C%22%2C%5C%22vm%5C%22%3A%5C%22nw%5C%22%2C%5C%22countryNum%5C%22%3A%5C%22156%5C%22%2C%5C%22m%5C%22%3A%5C%22pc%5C%22%2C%5C%22page%5C%22%3A1%2C%5C%22n%5C%22%3A48%2C%5C%22q%5C%22%3A%5C%22%25E9%2594%25AE%25E7%259B%2598%5C%22%2C%5C%22qSource%5C%22%3A%5C%22url%5C%22%2C%5C%22pageSource%5C%22%3A%5C%22a21bo.jianhua%2Fa.201856.d13%5C%22%2C%5C%22tab%5C%22%3A%5C%22all%5C%22%2C%5C%22pageSize%5C%22%3A48%2C%5C%22totalPage%5C%22%3A100%2C%5C%22totalResults%5C%22%3A4800%2C%5C%22sourceS%5C%22%3A%5C%220%5C%22%2C%5C%22sort%5C%22%3A%5C%22_coefp%5C%22%2C%5C%22bcoffset%5C%22%3A%5C%22%5C%22%2C%5C%22ntoffset%5C%22%3A%5C%22%5C%22%2C%5C%22filterTag%5C%22%3A%5C%22%5C%22%2C%5C%22service%5C%22%3A%5C%22%5C%22%2C%5C%22prop%5C%22%3A%5C%22%5C%22%2C%5C%22loc%5C%22%3A%5C%22%5C%22%2C%5C%22start_price%5C%22%3Anull%2C%5C%22end_price%5C%22%3Anull%2C%5C%22startPrice%5C%22%3Anull%2C%5C%22endPrice%5C%22%3Anull%2C%5C%22itemIds%5C%22%3Anull%2C%5C%22p4pIds%5C%22%3Anull%2C%5C%22p4pS%5C%22%3Anull%2C%5C%22categoryp%5C%22%3A%5C%22%5C%22%2C%5C%22ha3Kvpairs%5C%22%3Anull%2C%5C%22myCNA%5C%22%3A%5C%22QSD0HThygTMCAXL2xCRlUDLD%5C%22%7D%22%7D'

#查询参数
data={
'jsv':' 2.7.4',
'appKey':' 12574478',
't':' 1737377813183',
'sign':' 02de25e573c399e74129ab11b8af7411',
'api':' mtop.relationrecommend.wirelessrecommend.recommend',
'v':' 2.0',
'timeout':' 10000',
'type':' jsonp',
'dataType':' jsonp',
'callback':' mtopjsonp5',
'data':' {"appId":"34385","params":"{\"device\":\"HMA-AL00\",\"isBeta\":\"false\",\"grayHair\":\"false\",\"from\":\"nt_history\",\"brand\":\"HUAWEI\",\"info\":\"wifi\",\"index\":\"4\",\"rainbow\":\"\",\"schemaType\":\"auction\",\"elderHome\":\"false\",\"isEnterSrpSearch\":\"true\",\"newSearch\":\"false\",\"network\":\"wifi\",\"subtype\":\"\",\"hasPreposeFilter\":\"false\",\"prepositionVersion\":\"v2\",\"client_os\":\"Android\",\"gpsEnabled\":\"false\",\"searchDoorFrom\":\"srp\",\"debug_rerankNewOpenCard\":\"false\",\"homePageVersion\":\"v7\",\"searchElderHomeOpen\":\"false\",\"search_action\":\"initiative\",\"sugg\":\"_4_1\",\"sversion\":\"13.6\",\"style\":\"list\",\"ttid\":\"600000@taobao_pc_10.7.0\",\"needTabs\":\"true\",\"areaCode\":\"CN\",\"vm\":\"nw\",\"countryNum\":\"156\",\"m\":\"pc\",\"page\":1,\"n\":48,\"q\":\"%E9%94%AE%E7%9B%98\",\"qSource\":\"url\",\"pageSource\":\"a21bo.jianhua/a.201856.d13\",\"tab\":\"all\",\"pageSize\":48,\"totalPage\":100,\"totalResults\":4800,\"sourceS\":\"0\",\"sort\":\"_coefp\",\"bcoffset\":\"\",\"ntoffset\":\"\",\"filterTag\":\"\",\"service\":\"\",\"prop\":\"\",\"loc\":\"\",\"start_price\":null,\"end_price\":null,\"startPrice\":null,\"endPrice\":null,\"itemIds\":null,\"p4pIds\":null,\"p4pS\":null,\"categoryp\":\"\",\"ha3Kvpairs\":null,\"myCNA\":\"QSD0HThygTMCAXL2xCRlUDLD\"}"}',
}

#发送请求
response = requests.get(url=url, params=data, headers=headers)


