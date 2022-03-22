// Fill out your copyright notice in the Description page of Project Settings.


#include "KM_GAHelperFunctions.h"
#include "AbilitySystemGlobals.h"

void UKM_GAHelperFunctions::SetupAbilitySystem(AActor* Target, UAbilitySystemComponent* AbilitySystem, TArray<TSubclassOf<class UGameplayAbility>> AbilityList)
{
    if (AbilitySystem && Target)
    {
        if (Target->GetLocalRole() == ROLE_Authority) 
        {
            int32 inputID(0);
            if (AbilityList.Num() > 0)
            {
                for (auto Ability : AbilityList)
                {
                    if (Ability)
                    {
                        AbilitySystem->GiveAbility(FGameplayAbilitySpec(Ability.GetDefaultObject(), 1, inputID++));
                    }
                }
            }
        }
        AbilitySystem->InitAbilityActorInfo(Target, Target);
    }
}

void UKM_GAHelperFunctions::InitAbilitySystem(AActor* Target, UAbilitySystemComponent* AbilitySystem)
{
    if (AbilitySystem && Target)
    {
        AbilitySystem->InitAbilityActorInfo(Target, Target);
    }
}

void UKM_GAHelperFunctions::RefreshAbilityActorInfo(UAbilitySystemComponent* AbilitySystem)
{
    if (AbilitySystem)
    {
        AbilitySystem->RefreshAbilityActorInfo();
    }
}

void UKM_GAHelperFunctions::AddGameplayTags(UGameplayAbility* Ability, const FGameplayTagContainer GameplayTags)
{
    if (Ability) 
    {
        UAbilitySystemComponent* Comp = Ability->GetAbilitySystemComponentFromActorInfo();

        Comp->AddLooseGameplayTags(GameplayTags);
    }
}

void UKM_GAHelperFunctions::RemoveGameplayTags(UGameplayAbility* Ability, const FGameplayTagContainer GameplayTags)
{
    if (Ability) 
    {
        UAbilitySystemComponent* Comp = Ability->GetAbilitySystemComponentFromActorInfo();

        Comp->RemoveLooseGameplayTags(GameplayTags);
    }
}

void UKM_GAHelperFunctions::InitAttributeSet(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UAttributeSet> Attributes, UAttributeSet*& OutAttribute)
{
    if (AbilitySystem) 
    {
        const auto* ret = AbilitySystem->InitStats(Attributes, nullptr);
        // ‚±‚±‚Ü‚Å‚µ‚Äconst‚ð‚Í‚¸‚·‚±‚Æ‚ÉˆÓ–¡‚Í‚ ‚é‚Ì‚©c
        for (auto attr : AbilitySystem->GetSpawnedAttributes()) {
            if (attr == ret) {
                OutAttribute = attr;
            }
        }
        return;
    }
    OutAttribute = nullptr;
    return;
}

void UKM_GAHelperFunctions::SetReplicationModeFull(UAbilitySystemComponent* AbilitySystem)
{
    if (AbilitySystem)
    {
        AbilitySystem->SetReplicationMode(EGameplayEffectReplicationMode::Full);
    }
}

void UKM_GAHelperFunctions::SetReplicationModeMixed(UAbilitySystemComponent* AbilitySystem)
{
    if (AbilitySystem)
    {
        AbilitySystem->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);
    }
}

void UKM_GAHelperFunctions::SetReplicationModeMinimal(UAbilitySystemComponent* AbilitySystem)
{
    if (AbilitySystem)
    {
        AbilitySystem->SetReplicationMode(EGameplayEffectReplicationMode::Minimal);
    }
}

void UKM_GAHelperFunctions::GetAbilityLevel(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UGameplayAbility> Class, int& Level)
{
    if (AbilitySystem)
    {
        Level = AbilitySystem->FindAbilitySpecFromClass(Class)->Level;
    }
}

void UKM_GAHelperFunctions::SetAbilityLevel(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UGameplayAbility> Class, int Level)
{
    if (AbilitySystem)
    {
        AbilitySystem->FindAbilitySpecFromClass(Class)->Level = Level;
    }
}

void UKM_GAHelperFunctions::IncrementAbilityLevel(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UGameplayAbility> Class)
{
    if (AbilitySystem)
    {
        AbilitySystem->FindAbilitySpecFromClass(Class)->Level++;
    }
}
