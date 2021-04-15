import streamlit as st 
import pandas as pd 
from datetime import datetime 
import matplotlib as pyplot
import sqlite3
import plotly.graph_objects as go


def main():
    ### Database Functions ###
    #conn = sqlite3.connect('bot-data.db')
    conn = sqlite3.connect('bot-data-14Apr.db')
    c = conn.cursor()

    def create_table():
        #c.execute('CREATE TABLE IF NOT EXISTS botelection(name TEXT,position TEXT,category TEXT,electdate DATE)')
        c.execute('CREATE TABLE IF NOT EXISTS botelection(name TEXT,position TEXT,category TEXT, electdate DATE)')
    
    def add_vote(name,position,category,electdate):
        c.execute('INSERT INTO botelection(name,position,category,electdate) VALUES (?,?,?,?)',(name,position,category,electdate))
        #c.execute('INSERT INTO botelection(name,position,category,code,electdate) VALUES (?,?,?,?)',(name,position,category,code,electdate))
        conn.commit()

    def view_all_vote():
        c.execute('SELECT * FROM botelection')
        data = c.fetchall()
        return data

    def validate_code(code):
        c.execute('SELECT * FROM botelection WHERE code="{}"'.format(code))
        data = c.fetchall()
        return data

    def get_vote_by_name(author):
        c.execute('SELECT * FROM botelection WHERE name="{}"'.format(name))
        data = c.fetchall()
        return data

    def delete_vote(position):
        c.execute('DELETE FROM botelection WHERE position="{}"'.format(position))
        conn.commit()
    
    def elected(position):
        rows = view_all_vote()
        df_all = pd.DataFrame(rows, columns=['name','position','category','date'])

        #chairman_result = df_all.loc[df_all['position'] == 'President & Chairman']
        winner_result = df_all.loc[df_all['position'] == position ]
        name_of_elected = winner_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])
        #name_chairman = name_chairman.set_index('name')

        ### get highest vote
        highest = name_of_elected['total'].max()
        winner = name_of_elected[name_of_elected['total'] == highest]
        winner_shape = winner.shape[0]

        ### Name of Elected Board member
        elected_name = winner['name'].to_string(index=False)
        #st.write(winner_name)
        
        ### Council of Elected Board member ###
        #winner_council = winner_result['Council'].iloc[0]
        #chr_council = pres_name['Council'].iloc[0]
        #chr_name = pres_name['FullName'].iloc[0]
        #st.write(chair_winner_council)
        #st.write(chr_name)

        ### Get information of Elected Boardmember: FullName, LastName, FirstName, Council, Type  ###
        elected_info = df.query('FullName == @elected_name')
        #st.write(chairman_winner)

        return name_of_elected, elected_name, elected_info, winner_shape

### ---- End Database functions ---- ###

### ---- Layout ---- ###

    st.title('PBS 56th Annual Membership Meeting')
    menu = ["Board Execom Election", "Get Election Results"]

    choice = st.sidebar.selectbox("Menu", menu)
    
    ### ADDED ###
    create_table()

    if choice == "Board Execom Election":
        st.header('BOT Execom Election')
        tophead = st.beta_container()
        chairman = st.beta_container()
        vice_chairman = st.beta_container()
        secretary = st.beta_container()
        member1 = st.beta_container()
        member2 = st.beta_container()
        results = st.beta_container()

        df = pd.read_csv('bot.csv')
        
        # with tophead:
        #     name = df['FullName']
        #     x = df.shape[0]
        #     st.write('\n')

        #     nominees = st.beta_expander("Names of Nominees / Total Count = " + str(x))
        #     nominees.write(df)
        #     st.markdown("""
        #             \n \n \n
        #     """)
        #     st.write('\n')

        df_new = df.copy()

        with chairman:
            xp_chairman = st.beta_expander('Elect President & Chairman')
            with xp_chairman:
                chair_FullName = df_new['FullName']
                chair_Council = df_new['Council']
                chair_FullName_Council = chair_FullName + ' , ' + chair_Council
                chair = st.selectbox('Select New PBS President and Chairman:', chair_FullName_Council)
                chair = chair.split(" , ")

                chair_title = "President & Chairman"
                col1,col2 = st.beta_columns(2)
                with col1:
                    chair_button = col1.button("VOTE for President & Chairman")
                    if chair_button:
                        add_vote(chair[0],chair_title,chair[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")

                st.markdown("""
                    \n
                    \n
                    \n
                """)

        with vice_chairman:
            xp_vice_chairman = st.beta_expander('Elect Vice President & Vice Chairman')
            ### Halt Processing ###
            
            with xp_vice_chairman:

                vice_chairman_agree = st.checkbox("Proceed")

                if vice_chairman_agree:

                    ### Get Winner for President & Chairman ###
                    chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                    
                    if hchair > 2:
                        st.write(hchair)
                        st.write("Break the tie in President and Chairman.")
                    else:
                        chairman_council = chairman_info['Council'].iloc[0]  # Council

                        ### Search and remove Name and Council from dataset and create new one ###
                        vice_chair = df_new.query('FullName != @chairman_name and Council != @chairman_council')
                        vice_chair = vice_chair.reset_index(drop=True)
                        vice_chair_FullName = vice_chair['FullName']
                        vice_chair_Council = vice_chair['Council']
                        vice_chair_FullName_Council = vice_chair_FullName + ' , ' + vice_chair_Council
                        vice_chair = st.selectbox('Select New PBS Vice-President and Vice-Chairman:', vice_chair_FullName_Council)
                        vice_chair = vice_chair.split(" , ")

                        vice_chair_title = "Vice-President & Vice-Chairman"
                        col1,col2 = st.beta_columns(2)
                        with col1:
                            vice_chair_button = col1.button("VOTE for Vice-President & Vice-Chairman")
                            if vice_chair_button:
                                add_vote(vice_chair[0],vice_chair_title,vice_chair[1],datetime.date(datetime.now()))
                                col1.success(f"Vote successful.")
                        with col2:
                            col2.warning(f"Select nominee then click **Submit Vote** once.")

                st.markdown("""
                    \n
                    \n
                    \n
                """)

        with secretary:
            xp_secretary = st.beta_expander('Elect Corporate Secretary')
            with xp_secretary:
                
                ### Get values for Chairman and Council ###
                chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                chairman_council = chairman_info['Council'].iloc[0]

                ### Get Winner for Vice-President & Vice-Chairman ###
                vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
                vice_chairman_council = vice_chairman_info['Council'].iloc[0]

                ### Search and remove Name and Council from dataset and create new one ###
                secretary = df_new.query('FullName != @vice_chairman_name and Council != @vice_chairman_council and Council != @chairman_council')
                secretary = secretary.reset_index(drop=True)
                secretary_FullName = secretary['FullName']
                secretary_Council = secretary['Council']
                secretary_FullName_Council = secretary_FullName + ' , ' + secretary_Council
                secretary = st.selectbox('Select New Corporate Secretary:', secretary_FullName_Council)
                secretary = secretary.split(" , ")

                secretary_title = "Corporate Secretary"
                col1,col2 = st.beta_columns(2)
                with col1:
                    vice_chair_button = col1.button("VOTE for Corporate Secretary")
                    if vice_chair_button:
                        add_vote(secretary[0],secretary_title,secretary[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")
                
                st.markdown("""
                    \n
                    \n
                    \n
                """)

        with member1:
            xp_member1 = st.beta_expander('Select Member 1')
            with xp_member1:
                ### Get values for Chairman and Council ###
                chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                chairman_council = chairman_info['Council'].iloc[0]

                ### Get Winner for Vice-President & Vice-Chairman ###
                vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
                vice_chairman_council = vice_chairman_info['Council'].iloc[0]

                ### Get Winner Corporate Secretary ###
                secretary_election_result, secretary_name, secretary_info, shape_sec = elected("Corporate Secretary")
                
                #st.write(shape_sec)
                # if shape_sec > 1:
                #     st.write(secretary_election_result)
                #     #secretary_council = secretary_info['Council'].iloc[0]
                #     #secretary_council1 = secretary_info['Council'].iloc[1]
                # else:
                #     secretary_council = secretary_info['Council'].iloc[0]

                ### Search and remove Name and Council from dataset and create new one ###
                # member1 = df_new.query('FullName != @vice_chairman_name and Council != @vice_chairman_council and Council != @chairman_council ' +
                # ' and Council != @secretary_council')
                # member1 = member1.reset_index(drop=True)
                # member1_FullName = member1['FullName']
                # member1_Council = member1['Council']
                # member1_FullName_Council = member1_FullName + ' , ' + member1_Council
                # member1 = st.selectbox('Select Member One:', member1_FullName_Council)
                # member1 = member1.split(" , ")

                # member1_title = "Member"
                # col1,col2 = st.beta_columns(2)
                # with col1:
                #     member1_button = col1.button("VOTE for Member One")
                #     if member1_button:
                #         add_vote(member1[0],member1_title,member1[1],datetime.date(datetime.now()))
                #         col1.success(f"Vote successful.")
                # with col2:
                #     col2.warning(f"Select nominee then click **Submit Vote** once.")
                
                st.markdown("""
                    \n
                    \n
                    \n
                """)

        with member2:
            xp_member2 = st.beta_expander('Elect Member 2')
            with xp_member2:
                # df_member2 = df.copy()

                # member1_name = df_member2.loc[df_member2['FullName'] == member1]
                # #st.write(member1_name)
                # mem1_name = member1_name['FullName'].iloc[0]
                # mem1_council = member1_name['Council'].iloc[0]
                # #st.write(mem1_name, mem1_council)

                # # #st.write(vcn, vccn)
                # df_member2 = df_new.query('FullName != @vice_chair_name '\
                # + 'and FullName != @pres and FullName != @sc_name '\
                # + 'and FullName != @mem1_name ')
                # #df_member1
                # #df_member1
                # df_member2 = df_member2.reset_index(drop=True)

                # member2_name = df_member2['FullName']
                # # # mem1cn = df_mem1['Council'].iloc[0]
                # member2 = st.selectbox('Select New Member:', member2_name) # df_mem1)
                # member2_title = "Member"

                # member2_name = df_member2.loc[df_member2['FullName'] == member2]
                # mem2_name = member2_name['FullName'].iloc[0]
                # mem2_council = member2_name['Council'].iloc[0]
                #st.write(member2_council)
                st.markdown("""
                    \n
                    \n
                    \n
                """) 
        
    else:
        st.subheader("RESULTS OF EXECOM ELECTION")
        rows = view_all_vote()

        df_all = pd.DataFrame(rows, columns=['name','position','category','date'])

        #st.subheader('President & Chairman')
        chairman_result = df_all.loc[df_all['position'] == 'President & Chairman']
        name_chairman = chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])
        name_chairman = name_chairman.set_index('name')
        xp_chairman = st.beta_expander('President & Chairman')
        with xp_chairman:
            st.write(name_chairman)
        #st.write(name_chairman)
        st.bar_chart(name_chairman['total'])

        #st.subheader('Vice-President & Vice-Chairman')
        vicechairman_result = df_all.loc[df_all['position'] == 'Vice-President & Vice-Chairman']
        name_vicechairman = vicechairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'})
        name_vicechairman = name_vicechairman.set_index('name')
        xp_vicechairman = st.beta_expander('Vice-President & Vice-Chairman')
        with xp_vicechairman:
            st.write(name_vicechairman)
        #st.write(name_vicechairman)
        st.bar_chart(name_vicechairman['total'])


        # st.subheader('Corporate Secretary')
        secretary_result = df_all.loc[df_all['position'] == 'Corporate Secretary']
        name_secretary = secretary_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'})

        ### get highest vote
        highest = name_secretary['total'].max()
        winner = name_secretary[name_secretary['total'] == highest]
        st.write(highest)
        st.write(winner.shape[0])

        #name_secretary = secretary_result.value_counts(subset=['name'])
        name_secretary = name_secretary.set_index('name')
        xp_secretary = st.beta_expander('Corporate Secretary')
        with xp_secretary:
            st.write(name_secretary)
        #st.write(name_secretary)
        #st.bar_chart(name_secretary)
        st.bar_chart(name_secretary['total'])

        
        #st.subheader('Member')
        
        member1_result = df_all.loc[df_all['position'] == 'Member']
        name_member = member1_result.groupby(['name'])['position'].count().reset_index().rename(columns={'position':'total'})
        name_member = name_member.set_index('name')
        xp_member = st.beta_expander('Member')
        with xp_member:
            st.write(name_member)
        st.bar_chart(name_member['total'])

        tot = st.beta_expander("All Votes Here")
        with tot:
            st.write(df_all)



if __name__ == '__main__':
	main()