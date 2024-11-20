#
# import pandas as pd
#
# from datetime import date, timedelta
# # get current montth day
# today = date.today()
#
# month_before = today - timedelta(days=60)
# month_after = today + timedelta(days=30)
#
#
# pd_dr = pd.date_range(start=month_before, end=month_after, freq="D")
#
#
# pom_df = pom_df.reindex(pd_dr)
# hours_df = hours_df.reindex(pd_dr)
# ci_df = ci_df.reindex(pd_dr)
#
# fig, ax  = plt.subplots(3, figsize=(20 ,8), sharex=True)
#
# ax[0].tick_params(axis='x', labelsize=10, rotation=30)
#
# ax[0].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
# ax[0].set_title("Number of Commits per day")
# b c =ax[0].bar(pd_dr ,ci_df.commits , color="red", width=0.8, edgecolor="black")
#
# ax[1].tick_params(axis='x', labelsize=10, rotation=30)
# ax[1].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
# ax[1].set_title("Worked hours per day")
# contb c =ax[1].bar(pd_dr ,hours_df.duration_hour , color="blue", width=0.8, edgecolor="black")
#
#
#
# ax[2].tick_params(axis='x', labelsize=10, rotation=30)
# ax[2].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
# ax[2].set_title("Pomodoros per day")
# ax[2].set_xticks(pd_dr)
# pb c =ax[2].bar(pd_dr, pom_df, width=0.5)