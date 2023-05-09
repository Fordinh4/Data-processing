def output_1(filename):
    """Display the sorted list of group as well as written on a text file groups.txt"""
    # OUTPUT 1
    groups = []
    raw_group_match_data = []
    sorted_groups = {}
    fmt_data_1 = ""

    # I create a dictionary of list that contain the group name from A to H
    for group_name in range(ord("A"), ord("H") + 1):
        sorted_groups[chr(group_name)] = []


    with open(filename, "r") as file:
        list_of_lines = file.readlines()

    for line in list_of_lines[0:-1]:  # Use slicing to delete the blank line
        line = line.split(";")
        raw_group_match_data.append(line)
        groups.append(line[0:3])

    for country in groups:
        sorted_groups[country[0]].extend([country[1], country[2]])

    for group, countries in sorted_groups.items():
        fmt_data_1 += f"\nGroup {group}\n"
        sorted_groups.update({group: sorted(set(countries))})
        # I use set() method to covert the list which contain identical values to distinct values and sorted()
        # alphabetically it later

        for country in sorted(set(countries)):
            fmt_data_1 += f"{country}\n"

    print(fmt_data_1)
    return raw_group_match_data, sorted_groups, fmt_data_1


def output_2(raw_group_match_data, sorted_groups):
    """Display which team go in knock-out round and written on a text file knockout.txt"""

    # OUTPUT 2: The problem that I have with this output is it's not time efficient because it has to check the huge
    # data every time it need to check in for loops.

    yellow_cards = []
    with open("WC22-YellowCards.txt", "r") as file:
        for line in file:
            # strip() as slicing to avoid the \n at the end of each line
            yellow_cards.append(line.strip().split(";"))

    # I want to turn the dictionary of lists of value to dictionary of dictionary of value
    updated_sorted_group = {}
    sorted_yellow_cards = {}

    for group, teams in sorted_groups.items():
        temp = {}

        for item in teams:
            temp[item] = 0
            # I also want to make the dict below to store the yellow cards that each team have.
            sorted_yellow_cards[item] = 0
        updated_sorted_group[group] = temp

    # I sorted and calculate the total yellow cards for each country.
    for country, card in sorted_yellow_cards.items():

        for item in yellow_cards:

            if country == item[1]:

                if item[-2] == "Y":
                    # If it only yellow card, + 1 for that team
                    sorted_yellow_cards[country] += 1
                else:
                    # If it's red card
                    sorted_yellow_cards[country] += 4

    # I update the points for every team in each groups
    won_data = {}  # I want to update who won for later use
    scored_players = []  # This list is for Output 6

    for matches in raw_group_match_data:
        group = matches[0]
        first_team = matches[1]
        second_team = matches[2]
        score = matches[3]

        first_team_score = score[1: score.index(")")].split(",")
        second_team_score = score[(score.index(")") + 2): -1].split(",")
        # it's a list contain strings

        for team, team_score in [(first_team, first_team_score), (second_team, second_team_score)]:
            # Because the first_team_score is a list contain the strings which is the player number, I use it to
            # create a string to append to the list after

            for player_number in team_score:

                if player_number != "":
                    scored_players.append(f"{team} {player_number}")

        # I use len to calculate how many goals each team have.
        first_team_score_count = len(first_team_score)
        second_team_score_count = len(second_team_score)

        # I need to check the condition when len([""]) still count as 1 which is not what I want because I want 0
        if first_team_score == [""]:
            first_team_score_count = 0

        if second_team_score == [""]:
            second_team_score_count = 0

        # I compare the score between two team and also store the data of which team won
        if first_team_score_count > second_team_score_count:
            updated_sorted_group[group][first_team] += 3
            won_data[f"{first_team} vs {second_team}"] = f"{first_team}"

        elif first_team_score_count < second_team_score_count:
            updated_sorted_group[group][second_team] += 3
            won_data[f"{first_team} vs {second_team}"] = f"{second_team}"

        else:
            updated_sorted_group[group][first_team] += 1
            updated_sorted_group[group][second_team] += 1
            won_data[f"{first_team} vs {second_team}"] = f"draw"

    knockout_teams = {}
    for group, teams in updated_sorted_group.items():
        updated_sorted_group.update({group: dict(sorted(teams.items(), key=lambda x: x[1], reverse=True))})
        # I use sorted and lambda to sort the value inside the dictionary and x[1] mean that it only sort the value
        # but not the key. And reverse to sort from highest to lowest After that I need to use dict() because the
        # output of sorted() will be a list. And the reason I sorted it is that I want to pick the first biggest
        # number in each group.

    for group, teams in updated_sorted_group.items():
        first_team_won, second_team_won, third_team_won = list(teams)[:3]

        if updated_sorted_group[group][second_team_won] == updated_sorted_group[group][third_team_won]:
            # Because the first team won regardless, so I need to check the second and third team
            knockout_teams[first_team_won] = updated_sorted_group[group][first_team_won]

            for match, team_won in won_data.items():
                # I use the data in won_data which include the match between two teams and who won to check for the
                # condition which the second and third team share the same points.

                if f"{second_team_won} vs {third_team_won}" == match or f"{third_team_won} vs {second_team_won}" == match:

                    if second_team_won == team_won:
                        # If the second team won their head-to-head game, they are qualify.

                        knockout_teams[second_team_won] = updated_sorted_group[group][second_team_won]

                    elif third_team_won == team_won:
                        # Opposite condition to the above.

                        knockout_teams[third_team_won] = updated_sorted_group[group][third_team_won]

                    else:
                        # If these teams are draw, I will check their yellow cards.
                        if sorted_yellow_cards[second_team_won] < sorted_yellow_cards[third_team_won]:
                            knockout_teams[second_team_won] = updated_sorted_group[group][second_team_won]

                        else:
                            knockout_teams[third_team_won] = updated_sorted_group[group][third_team_won]

        else:
            # If the second and third team aren't having the same point, the first and second are qualify.
            knockout_teams[first_team_won] = updated_sorted_group[group][first_team_won]
            knockout_teams[second_team_won] = updated_sorted_group[group][second_team_won]

    sorted_teams = []
    fmt_data_2 = ""

    # I sort the team's name alphabetically 
    for team in knockout_teams.keys():
        sorted_teams.append(team)

    for team_name in sorted(sorted_teams):
        fmt_data_2 += "{:<12} {} pts\n".format(team_name, knockout_teams[team_name])

    print(fmt_data_2)

    return fmt_data_2, scored_players, yellow_cards


def output_3(filename):
    """Display the age average of each country and the age average overall as well as written on a text file ages.txt"""

    team_age = {}
    histogram = []  # For output 4
    players_info = {}  # For output 6

    with open(filename, encoding='UTF-8') as file:
        for line in file:
            item = line.strip().split(";")

            country = item[0][:-2].strip()
            # The reason I use strip in country is for the case like ["Ecuador 12"] where [:-2] will leave "Ecuador "
            # a space, so I use strip() to handle it.

            player_age = item[-1][(item[-1].index("d") + 2):-1]
            # For example, item[-1] = '30 March 1987 (aged 35)' and to get 35 out of that string, I use slicing from
            # the index of the letter "d" +2 to the position -1 which is ")"

            players_info[item[0]] = item[2]  # For output 6 because I need the players number

            # If that key not exist in the list => make an empty list. Else, append it
            if country not in team_age:
                team_age[country] = []  # Empty list for each key
                team_age[country].append(int(player_age))
                histogram.append(int(player_age))
            else:
                team_age[country].append(int(player_age))
                histogram.append(int(player_age))

    overall_ages = 0
    overall_players = 0
    for countries, ages in team_age.items():
        # I calculate the average age for each country.
        team_age[countries] = sum(ages) / len(ages)

        # These overall variables are using to calculate the average overall
        overall_ages += sum(ages)
        overall_players += len(ages)

    fmt_data_3 = ""
    for country in sorted(team_age.keys(), key=lambda x: x.lower()):
        fmt_data_3 += "{:<12} {:.2f} years\n".format(country, team_age[country])

    fmt_data_3 += "\n{:<12} {:.2f} years\n".format("Average Overall", (overall_ages / overall_players))

    print(fmt_data_3)
    return fmt_data_3, histogram, players_info


def output_4(age_data):
    """Display the histogram of the age as well as written on a text file histogram.txt"""

    histogram_dict = {}

    # Because the age ranging from 18 to 40-year-old, I use it to make key for my dict corresponding with value which
    # is 0
    for i in range(18, 41):
        histogram_dict[i] = 0

    # I count every time whenever I encounter the age that is the same as my key in histogram_dict
    for age in age_data:
        histogram_dict[age] += 1

    fmt_data_4 = ""
    for age, frequency in histogram_dict.items():
        stars = round(frequency / 5) * "*"

        # This is for the case where stars = "" because round(1/5) =  0 as an example.
        if stars == "":
            stars += "*"

        fmt_data_4 += "{} years ({:>2}){}\n".format(age, frequency, stars)

    print(fmt_data_4)
    return fmt_data_4


def output_6(players_info, scored_players):
    """Display the table of the players who score the highest as well as written on a text file scorer.txt"""
    
    player_goals = {}
    converted_scored_player = []

    # I convert from players number to players name
    for scored_player in scored_players:

        # There is case like "Canada X5" and I still count it as a goal for that player - Canada 5
        if "X" in scored_player:
            scored_player = scored_player.replace("X", "")

        for player_number, player_name in players_info.items():
            if scored_player == player_number:
                converted_scored_player.append(f"{player_name}|{player_number}")
                # I do this to easily extract the country and number later when formatting.
 
    for player_country in converted_scored_player:
        # If that key not exist in the list => it = 0. Else, += 1
        if player_country not in player_goals:
            player_goals[player_country] = 0
            player_goals[player_country] += 1

        else:
            player_goals[player_country] += 1

    fmt_data_6 = ""
    bars = "+{}+{}+{}+\n".format("-" * 9, "-" * 15, "-" * 30)

    fmt_data_6 += bars

    max_score = max(player_goals.values())
    for player_n_country, goals in player_goals.items():
        if goals == max_score:
            name = player_n_country.split("|")[0]
            country_number = player_n_country.split("|")[1]

            # I still need to separate the country and the player number, so I use the for loop
            number = ""
            country = ""
            for i in country_number:
                if i.isdigit():
                    number += i
                else:
                    country += i

            fmt_data_6 += "| {} goals | {:<14}| {:>2} {:<26}|\n".format(goals, country, number, name)
    fmt_data_6 += bars

    print(fmt_data_6)
    return fmt_data_6


def output_8(yellow_cards_data):
    """Display how many YC each country have in their match as well as written on a text file yellow.txt"""

    yellow_cards = {}

    for unsorted_match in yellow_cards_data:
        first_team, second_team = unsorted_match[0].split("-")
        yellow_card_team = unsorted_match[1]
        card_type = unsorted_match[-2]
        temp = 0

        # I use dict in dict in dict for this output
        if f"{first_team} vs {second_team}" not in yellow_cards:
            # If that dict is not in yellow_cards dict, it will make an empty dict
            yellow_cards[f"{first_team} vs {second_team}"] = {}

        # I need to check if the card type is red then it += 4 else += 1
        if card_type == "Y":
            temp += 1
        else:
            temp += 4

        # I did the same thing as above but I use temp to count how much YC each team have
        if yellow_card_team not in yellow_cards[f"{first_team} vs {second_team}"]:
            yellow_cards[f"{first_team} vs {second_team}"][first_team] = 0
            yellow_cards[f"{first_team} vs {second_team}"][second_team] = 0

            yellow_cards[f"{first_team} vs {second_team}"][yellow_card_team] += temp
        else:
            yellow_cards[f"{first_team} vs {second_team}"][yellow_card_team] += temp

    # I sorted the value of YC in each team
    for match, yellow_number in yellow_cards.items():
        yellow_cards[match] = (dict(sorted(yellow_number.items(), key=lambda x: x[1], reverse=True)))

    fmt_data_8 = ""
    for sorted_match, sorted_yellow_number in yellow_cards.items():
        fmt_data_8 += "{}\n".format(sorted_match)

        for team, yc in sorted_yellow_number.items():
            fmt_data_8 += "{}: {} YC\n".format(team, yc)
        fmt_data_8 += f"\n"

    print(fmt_data_8)
    return fmt_data_8


def update_file(file_data, file_name):
    """Updating the filename whenever calling it"""
    with open(file_name, "w", encoding='utf8') as file:
        file.write(file_data)


def main():

    raw_group_match_data, sorted_groups, output_1_file = output_1("WC22GroupMatches.txt")
    update_file(output_1_file, "groups.txt")

    output_2_file, scored_players, yellow_cards_data = output_2(raw_group_match_data, sorted_groups)
    update_file(output_2_file, "knockout.txt.")

    output_3_file, histogram_data, players_info = output_3("WC22Footballers.txt")
    update_file(output_3_file, "ages.txt")

    output_4_file = output_4(histogram_data)
    update_file(output_4_file, "histogram.txt")

    output_6_file = output_6(players_info, scored_players)
    update_file(output_6_file, "scorer.txt")

    output_8_file = output_8(yellow_cards_data)
    update_file(output_8_file, "yellow.txt")


if __name__ == "__main__":
    main()
