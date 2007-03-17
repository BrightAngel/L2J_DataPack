# Made by Mr. - Version 0.3 by DrLecter
import sys
from net.sf.l2j.gameserver.model.quest import State
from net.sf.l2j.gameserver.model.quest import QuestState
from net.sf.l2j.gameserver.model.quest.jython import QuestJython as JQuest

qn = "296_SilkOfTarantula"

TARANTULA_SPIDER_SILK = 1493
TARANTULA_SPINNERETTE = 1494
RING_OF_RACCOON = 1508
RING_OF_FIREFLY = 1509
ADENA = 57

class Quest (JQuest) :

 def __init__(self,id,name,descr): JQuest.__init__(self,id,name,descr)

 def onEvent (self,event,st) :
    htmltext = event
    if event == "30519-03.htm" :
      st.set("cond","1")
      st.setState(STARTED)
      st.playSound("ItemSound.quest_accept")
    elif event == "30519-06.htm" :
      st.takeItems(TARANTULA_SPINNERETTE,-1)
      st.exitQuest(1)
      st.playSound("ItemSound.quest_finish")
    elif event == "30548-02.htm" :
      if st.getQuestItemsCount(TARANTULA_SPINNERETTE) :
        htmltext = "30548-03.htm"
        st.giveItems(TARANTULA_SPIDER_SILK,15+st.getRandom(9))
        st.takeItems(TARANTULA_SPINNERETTE,1)
    elif event == "30519-09.htm" :
      st.exitQuest(1)
    return htmltext

 def onTalk (Self,npc,st):
   npcId = npc.getNpcId()
   htmltext = "<html><head><body>I have nothing to say you</body></html>"
   id = st.getState()
   if id == CREATED :
     st.set("cond","0")
   if npcId == 30519 :
     if int(st.get("cond"))==0 :
       if st.getPlayer().getLevel() >= 15 :
         if st.getQuestItemsCount(RING_OF_RACCOON)==st.getQuestItemsCount(RING_OF_FIREFLY)==0 :
           htmltext = "30519-08.htm"
         else:
           htmltext = "30519-02.htm"
       else:
         htmltext = "30519-01.htm"
         st.exitQuest(1)
     else :
       count = st.getQuestItemsCount(TARANTULA_SPIDER_SILK)
       if count == 0 :
         htmltext = "30519-04.htm"
       else :
         htmltext = "30519-05.htm"
         st.giveItems(ADENA,count*20)
         st.takeItems(TARANTULA_SPIDER_SILK,count)
   else :
     htmltext = "30548-01.htm"
   return htmltext

 def onKill (self,npc,st):
   n = st.getRandom(100)
   if n > 95 :
     st.giveItems(TARANTULA_SPINNERETTE,1)
     st.playSound("ItemSound.quest_itemget")
   elif n > 45 :
     st.giveItems(TARANTULA_SPIDER_SILK,1)
     st.playSound("ItemSound.quest_itemget")
   return

QUEST       = Quest(296,qn,"Silk Of Tarantula")
CREATED     = State('Start', QUEST)
STARTING    = State('Starting', QUEST)
STARTED     = State('Started', QUEST)
COMPLETED   = State('Completed', QUEST)

QUEST.setInitialState(CREATED)
QUEST.addStartNpc(30519)

CREATED.addTalkId(30519)
STARTING.addTalkId(30519)
COMPLETED.addTalkId(30519)

STARTED.addTalkId(30519)
STARTED.addTalkId(30548)

STARTED.addKillId(20394)
STARTED.addKillId(20403)
STARTED.addKillId(20508)

STARTED.addQuestDrop(20508,TARANTULA_SPIDER_SILK,1)
STARTED.addQuestDrop(20394,TARANTULA_SPINNERETTE,1)

print "importing quests: 296: Silk Of Tarantula"
