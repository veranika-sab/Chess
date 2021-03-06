from django import template
from app.models import Tournament
from app.models import Tour, MatchResult

register = template.Library()

@register.inclusion_tag('admin/app/tournament/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    generate_pairs = False
    #read about F
    if context.get('object_id'):
        tournament=Tournament.objects.get(id=context['object_id'])
        if MatchResult.objects.filter(tournament_tour__tournament__id=tournament.id, player_one_result=-1).exists():
            pass
        elif Tour.objects.filter(tournament__id=tournament.id, tour=tournament.tours_amount).exists():
            pass
        else:
            generate_pairs = True

    ctx = {
        'opts': opts,
        'onclick_attrib': (opts.get_ordered_objects() and change
                           and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                             and change and context.get('show_delete', True)),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                                     not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
        'generate_pairs': generate_pairs
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx
