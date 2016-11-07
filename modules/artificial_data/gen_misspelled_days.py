import re, collections

days_of_week = ['Mon', 'Mon.', 'Monday', 'Tues', 'Tues.', 'Tuesday', 'Wed', 'Wed.', 'Wednesday', 'Thurs', 'Thurs.',
                'Thursday', 'Fri', 'Fri.', 'Friday', 'Sat', 'Sat.', 'Saturday', 'Sun', 'Sun.', 'Sunday']

months = ['Jan', 'Jan.', 'January', 'Feb', 'Feb.', 'February', 'Mar', 'Mar.', 'March', 'Apr', 'Apr.', 'April',
          'June', 'Jun', 'Jun.', 'July', 'Jul', 'Jul.', 'August', 'Aug', 'Aug.', 'Sept', 'Sept.', 'September', 'Oct',
          'Oct.', 'October', 'Nov', 'Nov.', 'November', 'Dec', 'Dec.', 'December']

misc = ['next', 'last']

DAY_TAGS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
MONTH_TAGS = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']
MISC_TAGS = ['NEXT', 'LAST']

alphabet = 'abcdefghijklmnopqrstuvwxyz '
vowels = 'aeiouy'

alph = []
vow = []

def edits1(word):
   splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   at = [word + '@']
   deletes = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts = [a + c + b for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts + at)

def v_edits(word):
   splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces = [a + c + b[1:] for a, b in splits for c in vowels if b]
   inserts = [a + c + b for a, b in splits for c in vowels]
   return set(deletes + transposes + replaces + inserts)

#def known_edits2(word):
 #   return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

for w in days_of_week:
    alph.extend(list(edits1(w.lower())))
    vow.extend(list(v_edits(w.lower())))

for m in months:
    alph.extend(list(edits1(m.lower())))
    vow.extend(list(v_edits(m.lower())))

for m in misc:
    alph.extend(list(edits1(m.lower())))
    vow.extend(list(v_edits(m.lower())))


def iterate(f, l, tags):

    counter = 0;
    i = 0
    for w in l[:]:
        if counter == 3:
            i += 1
            counter = 0

        words = list(edits1(w.lower()))
        for w in words[:]:
            if len(w) > 2:
                f.write(w + '\t' + tags[i] + '\n')
        counter += 1


#take word
#run edits
#iter thru edits
#put tab and corresponding tag
def create_tsv_file():
    t = open('new_alph.tsv', 'w')
    iterate(t, days_of_week, DAY_TAGS)
    iterate(t, months, MONTH_TAGS)

    # May special case
    may = list(edits1('may'))
    for m in may[:]:
        if len(m) > 2:
            t.write(m + '\t' + 'MAY' + '\n')

    #iter thru misc
    i = 0
    for m in misc[:]:
        l = list(edits1(m))
        for word in l[:]:
            t.write(word + '\t' + MISC_TAGS[i] + '\n')
        i += 1

    t.close()


def create_txt_file():
    f = open('days_and_months.txt', 'w')
    for q in vow:
        f.write(q + '\n')

    f.close()

create_tsv_file()