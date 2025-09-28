from fastapi import APIRouter

from models.playbooks import Playbook

router = APIRouter()


@router.get('/', response_model=list[Playbook])
def get_playbooks() -> list[Playbook]:
    return [
        Playbook(
            name='Kickoff',
            steps=[
                'Align scope with sponsor',
                'Invite core team',
                'Publish kickoff agenda',
            ],
        ),
        Playbook(
            name='Monthly Close',
            steps=[
                'Collect vendor invoices',
                'Reconcile spend in Genie',
                'Update Tableau dashboards',
            ],
        ),
    ]
