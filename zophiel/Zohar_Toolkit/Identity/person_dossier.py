import time

class IdentityHunter:
    def __init__(self):
        self.dork_templates = [
            'site:linkedin.com "{name}"',
            'site:facebook.com "{name}"',
            'site:instagram.com "{name}"',
            'site:twitter.com "{name}"',
            '"{name}" filetype:pdf',
            '"{name}" "resume"',
            '"{name}" "cv"',
            '"{name}" "email"',
            '"{name}" "phone"',
            'intitle:"{name}"'
        ]

    def build_dossier(self, name):
        """
        Aggregates public information to build a target dossier.
        """
        print(f"[*] Initializing Dossier Build for: {name.upper()}")
        
        # 1. Generate Google Dorks
        print("\n[*] Generating Search Vectors (Google Dorks)...")
        dorks = self._generate_dorks(name)
        for i, dork in enumerate(dorks, 1):
            encoded_dork = dork.replace(' ', '+').replace('"', '%22')
            print(f"    {i}. https://www.google.com/search?q={encoded_dork}")
            
        # 2. Username Permutation Generation
        print("\n[*] Generating Potential Usernames...")
        usernames = self._generate_usernames(name)
        print(f"    Targeting: {', '.join(usernames[:5])}...")

        # 3. Deep Search Instructions
        print("\n[*] MANUAL CHECK INSTRUCTIONS:")
        print("    1. Run Dorks 1-3 to identify primary social profiles.")
        print("    2. Extract 'Current City' and 'Employer' from LinkedIn.")
        print("    3. Cross-reference Username matches on Sherlock/Maigret.")

    def _generate_dorks(self, name):
        return [t.format(name=name) for t in self.dork_templates]

    def _generate_usernames(self, name):
        """
        Creates common username formats based on the real name.
        e.g., John Doe -> johndoe, jdoe, john.doe
        """
        parts = name.lower().split()
        if len(parts) < 2:
            return [name.lower()]
        
        first, last = parts[0], parts[-1]
        return [
            f"{first}{last}",
            f"{first}.{last}",
            f"{first}_{last}",
            f"{first}{last[0]}",
            f"{first[0]}{last}",
            f"{last}{first}",
            f"iam{first}{last}"
        ]

if __name__ == "__main__":
    hunter = IdentityHunter()
    target = input("Enter Target Name (e.g., John Doe): ")
    hunter.build_dossier(target)
