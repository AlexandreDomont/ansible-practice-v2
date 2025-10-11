#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os

DOCUMENTATION = """
---
module: mon_module
short_description: Crée un fichier avec un message personnalisé
description:
  - Ce module écrit un message de salutation dans un fichier.
  - Il prend en compte l'idempotence, le mode check, et fournit un diff si le fichier change.
options:
  name:
    description:
      - Le nom de la personne à saluer.
    required: true
    type: str
  path:
    description:
      - Le chemin du fichier à créer ou mettre à jour.
    required: true
    type: str
author:
  - "Moi !!"
"""

EXAMPLES = """
- name: Créer un message dans un fichier
  mon_module:
    name: Alice
    path: /tmp/bonjour.txt
"""

RETURN = """
message:
  description: Résultat de l'exécution
  type: str
  returned: always
diff:
  description: Ancien vs nouveau contenu (si applicable)
  type: dict
  returned: when changed
"""

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            path=dict(type="str", required=True),
        ),
        supports_check_mode=True
    )

    name = module.params["name"]
    path = module.params["path"]

    # Nouveau contenu généré
    new_content = f"👋 Bonjour {name} ! Passe une excellente journée avec Ansible. 🚀\n"
    old_content = ""

    # Lire l'ancien contenu s'il existe
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                old_content = f.read()
        except Exception as e:
            module.fail_json(msg=f"Erreur de lecture du fichier : {str(e)}")

    # Vérifier s’il y a une réelle différence
    content_changed = old_content != new_content

    # Mode check : on affiche le diff mais on ne change rien
    if module.check_mode:
        module.exit_json(
            changed=content_changed,
            message="Simulation : le fichier serait mis à jour." if content_changed else "Simulation : aucun changement.",
            diff={"before": old_content, "after": new_content} if content_changed else {}
        )

    # Si le contenu est déjà identique → rien à faire
    if not content_changed:
        module.exit_json(
            changed=False,
            message="Aucun changement nécessaire. Le fichier est déjà à jour."
        )

    # Sinon, on écrit le nouveau contenu
    try:
        with open(path, "w") as f:
            f.write(new_content)
    except Exception as e:
        module.fail_json(msg=f"Erreur d'écriture du fichier : {str(e)}")

    # Message visible dans le callback (stdout)
    print(f"🎉 Nouveau message pour {name} écrit dans {path}")

    # Fin : on informe Ansible que le contenu a changé
    module.exit_json(
        changed=True,
        message=f"Fichier {path} mis à jour pour {name}.",
        diff={"before": old_content, "after": new_content}
    )

if __name__ == "__main__":
    main()
