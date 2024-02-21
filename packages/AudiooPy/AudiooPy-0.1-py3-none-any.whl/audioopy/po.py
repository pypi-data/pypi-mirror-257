import sys
import gettext
import locale
import logging
import os

# ----------------------------------------------------------------------------


class textTranslate(object):
    """Fix the domain to translate messages and to activate the gettext method.

    The locale is used to set the language, default is 'en'.
    The path to search for a domain translation is the one of the 'po' folder.

    :Example:

        >>> _ = textTranslate().translation().gettext
        >>> my_string = _("Some string in the domain.")

    """

    def __init__(self, lang="en"):
        """Create a textTranslate instance.

        :param lang: (str) The default language to fall back on

        """
        self.__po = "po"
        self.__default = [lang]
        self.__lang = textTranslate.get_lang_list(lang)

    # ------------------------------------------------------------------------

    def translation(self, domain="audioopy"):
        """Create the GNUTranslations for a given domain.

        A domain corresponds to a .po file of the language in the 'po' folder
        of the package.

        :param domain: (str) Name of the domain.
        :returns: (GNUTranslations)

        """
        try:
            # Install translation for the local language + English
            t = gettext.translation(domain, self.__po, self.__lang)
            t.install()
            return t
        except:
            try:
                # Install translation for English only
                t = gettext.translation(domain, self.__po, self.__default)
                t.install()
                return t
            except IOError:
                pass

        # No language installed. The messages won't be translated;
        # at least they are simply returned.
        return gettext.Catalog(domain, self.__po)

    # ------------------------------------------------------------------------

    @staticmethod
    def get_lang_list(default="en"):
        """Return the list of languages depending on the default locale.

        At a first stage, the language is fixed with the default locale.
        the given default language is then either appended to the list or used.

        :param default: (str) The default language.
        :return: (list) Installed languages.

        """
        lc = list()
        lc.append(default)
        try:
            if sys.version_info < (3, 6):
                # Only the locale is needed, not the returned encoding.
                sys_locale, _ = locale.getdefaultlocale()
            else:
                sys_locale, _ = locale.getlocale()
            if sys_locale is None:
                # Under macOS, the locale is defined differently compared to
                # other systems, then Python cannot capture a valid value.
                # So, try something else:
                sys_locale = os.getenv("LANG")

            if sys_locale is not None:
                if "_" in sys_locale:
                    sys_locale = sys_locale[:sys_locale.index("_")]
                lc.insert(0, sys_locale)
            else:
                logging.warning("The Operating System didn't defined a valid default locale.")
                logging.warning("It means that it assigns the language in a *** non-standard way ***.")
                logging.warning("This problem can be fixed by setting properly the 'LANG' "
                                "environment variable. See the documentation of your OS.")
                logging.warning("As a consequence, the language is set to its default value: "
                                "{:s}".format(lc[0]))

        except Exception as e:
            logging.error("Can't get the system default locale: {}".format(e))

        return lc

    # ------------------------------------------------------------------------

    def error(self, msg):
        """Return the error message from gettext with its number.

        :param msg: (str or int) Error identifier
        :return: (str) Translated message or message

        """
        _msg_id = ":ERROR -1: "
        # Format the input message
        if isinstance(msg, int):
            # Create the "msg_id" string of the po files
            _msg_id = ":ERROR " + "{:04d}".format(msg) + ": "
            # Translate
            try:
                translation = self.translation()
                return _msg_id + translation.gettext(_msg_id)
            except:
                return ":ERROR -1: " + str(msg)

        # Translate
        try:
            translation = self.translation()
            return _msg_id + translation.gettext(msg)
        except:
            return _msg_id + str(msg)


# ---------------------------------------------------------------------------


tt = textTranslate("en")
