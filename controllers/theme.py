from models.theme import ThemeModel
from datetime import datetime, timedelta

class ThemeController():

    def create_theme(release_time, theme, theme_inspire, theme_author):
        if (release_time.hour != 6 and release_time.hour != 20) or release_time.minute != 30 or release_time.second != 0:
            return "Incorrect release time."
        if ThemeModel.find_by_release_time(release_time):
            return "Theme is already there for that time! Try PUT for edit."
        if ThemeModel.find_by_theme(theme):
            return "Theme has alrady been used."

        try:
            new_theme = ThemeModel(release_time, theme, theme_inspire, theme_author)
            new_theme.save_to_db()
            return ""
        except:
            return "Error in creating and saving theme."

    def update_theme(release_time, theme, theme_inspire, theme_author):
        # don't allow themes to be edited after 5 minutes prior to it's release time.
        if (datetime.now() - release_time > timedelta(minutes=5)):
            return "What has past is past. Live the present, anticipate the future, and embrace the past" 

        if (release_time.hour != 6 and release_time.hour != 20) or release_time.minute != 30 or release_time.second != 0:
            return "Invalid release time."

        by_release_time = ThemeModel.find_by_release_time(release_time)
        if not by_release_time:
            return "Create theme for the release time first."

        by_theme = ThemeModel.find_by_theme(theme)
        if by_theme:
            if by_theme.id != by_release_time.id:
                return "Theme attempting to edit is already taken. Try a new theme."
        
        # update
        by_release_time.theme = theme
        by_release_time.theme_inspire = theme_inspire
        by_release_time.theme_author = theme_author
        try:
            by_release_time.save_to_db()
        except:
            return "Error saving updated theme."
        return ""

    def get_now():
        # retrieve fitting theme for the time 6:30 or 20:30
        current = datetime.now()
        release1 = datetime(current.year, current.month, current.day, 6, 30, 0)
        release2 = datetime(current.year, current.month, current.day, 20, 30, 0)
        yest_release2 = release2 - timedelta(days=1) 
        tmr_release1 = release1 + timedelta(days=1) 

        if current < release1:
            wanted_theme_time = yest_release2
        elif (current >= release1) and (current < release2):
            wanted_theme_time = release1
        elif current > release2 and current < tmr_release1:
            wanted_theme_time = release2
        else:
            return "Invalid time.", None

        wanted_theme = []
        wanted_theme.append(ThemeModel.find_by_release_time(wanted_theme_time))
        if not wanted_theme:
            return "Daily theme not available right now.", None
        else:
            return "", wanted_theme

    def browse(days):
        current = datetime.now()
        quantity = days * 2
        if quantity < 0:
            return "Cannot go to the future.", None
        elif quantity > ThemeModel.get_count(current):
            return "No more themes.", None
        else:
            lowbound_time = current - timedelta(days=days)
            highbound_time = current
            list_of_themes = ThemeModel.list_between_by_release_time(lowbound_time, highbound_time, quantity)
            if not list_of_themes:
                return "No more themes.", None
            return "", list_of_themes

    def get_for_day(year, month, day):
        release1 = datetime(year, month, day, 6, 30, 0)
        release2 = datetime(year, month, day, 20, 30, 0)
        result = []
        try:
            result.append(ThemeModel.find_by_release_time(release1))
            result.append(ThemeModel.find_by_release_time(release2))
        except:
            return "Error fetching ThemeModel for the specified day.", None
        return "", result

    def get_for_month(year, month):
        pass

