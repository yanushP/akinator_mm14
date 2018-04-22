import random as rand
 
 
class database:
 
    STATES_CNT = 4
    names = []
    questions = []
    marks = []
    state_quest = [[] for _ in range(STATES_CNT)]
    bad_questions = set([])
 
    def __init__(self, link='data.txt'):
        f = open(link)
        self.names = f.readline().split(' ')
        if self.names[-1][-1] == '\n':
            self.names[-1] = self.names[-1][:-1]
        for ln in f.readlines():
            self.marks.append([])
            ln = ln[:-1] if ln[-1] == '\n' else ln
            tm = ln.split(' ')
            cur_quest = ''
            cur_stat = tm[0]
            parse_marks = False
            need_divide = False
 
            for i in range(1, len(tm)):
                if parse_marks or (tm[i].isnumeric() and tm[i + 1].isnumeric()):
                    parse_marks = True
                    self.marks[-1].append(int(tm[i]))
                    if self.marks[-1][-1] > 4:
                        need_divide = True
                else:
                    cur_quest = cur_quest + tm[i] + ' '
            cur_quest = cur_quest[:-1] + '?'
            self.questions.append(cur_quest)
            if need_divide:
                for i in range(len(self.marks[-1])):
                    self.marks[-1][i] = self.marks[-1][i] // 2
            for c in cur_stat:
                if c.isnumeric():
                    self.state_quest[int(c)].append(len(self.questions) - 1)
 
    def set_bad_question(self, num):
        self.bad_questions.add(num)
 
    def generate_question(self, state, cur_questions, cur_people):
        questions = []
        for nm in self.state_quest[state]:
            if nm not in self.bad_questions and nm not in cur_questions:
                questions.append(nm)
        return questions[rand.randint(0, len(questions) - 1)] if len(questions) > 0 else -1
 
    def check_answer(self, person, question, ans):
        mark = self.marks[question][person]
        if ans == 0 and mark > 2:
            return True
        elif ans == 1 and mark < 2:
            return True
        elif ans == 2 and mark <= 2:
            return True
        elif ans == 3 and mark >= 2:
            return True
        elif ans == 4:
            return True
        else:
            return False
 
class kernel:
 
    PROFESSORS_CNT = 20
    people_steps = []
    quest_steps = []
    cur_step = 0
    already_ask = False
 
    def __init__(self, link='data.txt'):
        self.base = database(link)
        self.people_steps.append(range(len(self.base.names)))
        self.quest_steps.append([])
 
    def get_state(self):
        cnt_proff = 0
        cnt_stud = 0
        for v in self.people_steps[self.cur_step]:
            cnt_proff += 1 if v < self.PROFESSORS_CNT else 0
            cnt_stud += 0 if v < self.PROFESSORS_CNT else 1
        if cnt_proff >= 3 or cnt_stud >= 5:
            return 0 # start state
        elif cnt_proff < 3:
            return 1 # stud state
        elif cnt_stud < 5:
            return 2 # proff state
        elif cnt_proff + cnt_stud < 6:
            return 3 # final state
 
    def go_back(self, num=2):
        print("GOBAAAAAACK")
        while len(self.people_steps[self.cur_step]) <= num:
            self.people_steps.pop()
            self.quest_steps.pop()
            self.cur_step -= 1
            print ("[WARN]: GO BACK")
 
    def get_question(self, num):
        return self.base.questions[num]
 
    def get_name(self, num):
        return self.base.names[num]
 
    def ask(self):
        if len(self.people_steps[self.cur_step]) == 1:
            return -1, self.people_steps[-1][0]
        if len(self.people_steps[self.cur_step]) == 0:
            self.go_back(2)
        if self.already_ask:
            return self.question, -1
 
        for num_back in [3, 10, 25]:
            cur_state = self.get_state()
            self.question = self.base.generate_question(cur_state, self.quest_steps[-1], self.people_steps[-1])
            if self.question == -1:
                self.go_back(num_back)
                continue
            self.already_ask = True
            return self.question, -1
        print ("[ERROR]: too many bad answers")
        exit(0)
        return -1, -1
 
    def answer(self, res):
        self.already_ask = False
        self.cur_step += 1
        if res == 4:
            self.base.set_bad_question(self.question)
        self.quest_steps.append(list(self.quest_steps[-1]))
        self.quest_steps[-1].append(self.question)
        self.people_steps.append([])
        for p in self.people_steps[-2]:
            if self.base.check_answer(p, self.question, res):
                self.people_steps[-1].append(p)
        return 1