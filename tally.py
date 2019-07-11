import csv
import copy

def nonzero_min(l):
    copy = [x for x in l]
    while min(copy) == 0:
        copy.pop(copy.index(min(copy)))
    return min(copy)


presidential_candidates = []
vp_candidates = []
secretary_candidates = []

president_data = []
vp_data = []
secretary_data = []

president = ''
vp = ''
secretary = ''

# extract data
with open('sample-ballot.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_line = True
    for row in csv_reader:
        if first_line:
            first_line = False
            presidential_candidates = map(lambda x: x.split('[')[1][:-1], row[2:8])
            vp_candidates = map(lambda x: x.split('[')[1][:-1], row[8:16])
            secretary_candidates = map(lambda x: x.split('[')[1][:-1], row[16:28])
        else:
            president_rank_raw = row[2:8]
            president_rank = []
            for r in ['1st', '2nd', '3rd', '4th', '5th', '6th']:
                president_rank.append(president_rank_raw.index(r))
            president_data.append(president_rank)

            vp_rank_raw = row[8:16]
            vp_rank = []
            for r in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']:
                vp_rank.append(vp_rank_raw.index(r))
            vp_data.append(vp_rank)

            secretary_rank_raw = row[16:28]
            secretary_rank = []
            for r in ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']:
                secretary_rank.append(secretary_rank_raw.index(r))
            secretary_data.append(secretary_rank)

num_presidential_candidates = len(presidential_candidates)
num_vp_candidates = len(vp_candidates)
num_secretary_candidates = len(secretary_candidates)


def decide_office(raw_data, candidates, eliminated_start, office_title):
    data = copy.deepcopy(raw_data)
    eliminated = [x for x in eliminated_start]

    num_candidates = len(candidates)

    for round_number in range(num_candidates):
        for i in range(num_candidates):
            for e in eliminated:
                for i in range(len(data)):
                    ranking = data[i]
                    if ranking[0] == e:
                        data[i].pop(0)
                        data[i].append(e)


        totals = [0] * (num_candidates)
        for ranking in data:
            if(ranking[0] not in eliminated):
                totals[ranking[0]] += 1
            else:
                # this should never happen
                print("ERROR: Eliminated person getting a vote for some reason (see line 79)")

        print("Round {0} of {1} tallying:".format(round_number, office_title))
        for i in range(len(totals)):
            print("    {0}: {1} votes".format(candidates[i], totals[i]))
        if max(totals) > (len(data) / 2):
            winner = candidates[totals.index(max(totals))]
            return winner

        loser = totals.index(nonzero_min(totals))
        eliminated.append(loser)
        print("----{1} eliminated, with {2} votes.".format(round_number, candidates[loser], totals[loser]))
        
        for i in range(len(data)):
            ranking = data[i]

            if ranking[0] == loser:
                data[i].pop(0)
                data[i].append(loser)

        for e in eliminated:
            for i in range(len(data)):
                ranking = data[i]
                if ranking[0] == e:
                    data[i].pop(0)
                    data[i].append(e)


president = decide_office(president_data, presidential_candidates, [], 'presidential')
print("****{0} wins the presidency!****".format(president))

vp = decide_office(vp_data, vp_candidates, [vp_candidates.index(president)], 'VP')
print("****{0} wins VP!****".format(vp))

secretary = decide_office(secretary_data, secretary_candidates, [secretary_candidates.index(president), secretary_candidates.index(vp)], 'secretary')
print("****{0} wins secretary!****".format(secretary))

print('\n\n')
print("Summary: {0} is President, {1} is VP, {2} is Secretary").format(president, vp, secretary)
