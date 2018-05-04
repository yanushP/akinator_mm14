import random as rand
import io

NEED_DBG_INFO = False

def print_dbg(obj):
    if not NEED_DBG_INFO: return
    print(obj)

class database:
    def __init__(self, link='data.txt'):
        self.names = []
        self.questions = []
        self.marks = []
        self.bad_questions = set([])

        f = io.open(link, encoding='utf-8')
        self.names = f.readline().split(' ')
        if self.names[-1][-1] == '\n':
            self.names[-1] = self.names[-1][:-1]
        for ln in f.readlines():
            self.marks.append([])
            ln = ln[:-1] if ln[-1] == '\n' else ln
            tm = ln.split(' ')
            cur_quest = ''
            parse_marks = False
            need_divide = False

            for i in range(0, len(tm)):
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

    def set_bad_question(self, num):
        self.bad_questions.add(num)

    def generate_question(self, cur_questions, cur_people):
        questions = []
        qpc = []
        for nm in range(len(self.questions)):
            if nm not in self.bad_questions and nm not in cur_questions:
                questions.append(nm)

        for q in questions:
            cnt = -1
            for a in range(4):
                n_cnt = 0
                for p in cur_people:
                    if self.check_answer(p, q, a):
                        n_cnt += 1
                cnt = max(cnt, n_cnt)
            qpc.append((cnt, q))
        qpc.sort()
        print_dbg("qpc {}".format(qpc))
        return qpc[rand.randint(0, min(3, len(questions) - 1))][1]

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
    def __init__(self, link='data.txt'):
        self.people_steps = []
        self.quest_steps = []

        self.base = database(link)
        self.people_steps.append(range(len(self.base.names)))
        self.quest_steps.append([])
        self.already_ask = False

    def go_back(self, num=2):
        while len(self.people_steps[-1]) <= num:
            print_dbg("[WARN]: GO BACK")
            self.people_steps.pop()
            self.quest_steps.pop()
            print_dbg("after question {}".format(self.quest_steps))
            print_dbg("after people {}".format(self.people_steps))

    def get_question(self, num):
        return self.base.questions[num]

    def get_name(self, num):
        return self.base.names[num]

    def ask(self):
        if len(self.people_steps[-1]) == 1:
            print_dbg("have answer question {}".format(self.quest_steps))
            print_dbg("have answer people {}".format(self.people_steps))
            return -1, self.people_steps[-1][0]
        if len(self.people_steps[-1]) == 0:
            self.go_back(3)
        if self.already_ask:
            return self.question, -1
        print_dbg("ask question {}".format(self.quest_steps))
        print_dbg("ask people {}".format(self.people_steps))

        for num_back in [2, 3, 5, 7, 9, 11, 22, 44]:
            self.question = self.base.generate_question(self.quest_steps[-1], self.people_steps[-1])
            print_dbg("self.question {}".format(self.question))
            if self.question == -1:
                self.go_back(num_back)
                continue
            self.already_ask = True
            return self.question, -1
        print_dbg("[ERROR]: too many bad answers")
        exit(0)
        return -1, -1

    def answer(self, res):
        print_dbg("answer before question {}".format(self.quest_steps))
        print_dbg("answer before people {}".format(self.people_steps))
        self.already_ask = False
        if res == 4:
            self.base.set_bad_question(self.question)
        self.quest_steps.append(list(self.quest_steps[-1]))
        self.quest_steps[-1].append(self.question)
        self.people_steps.append([])
        for p in self.people_steps[-2]:
            if self.base.check_answer(p, self.question, res):
                self.people_steps[-1].append(p)
        print_dbg("answer after question {}".format(self.quest_steps))
        print_dbg("answer after people {}".format(self.people_steps))
        return 1
