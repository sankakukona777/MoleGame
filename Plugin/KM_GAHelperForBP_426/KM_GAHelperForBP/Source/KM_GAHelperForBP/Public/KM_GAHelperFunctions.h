// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"
#include "GameplayTagContainer.h"
#include "KM_GAHelperFunctions.generated.h"

/**
 * 
 */
UCLASS()
class KM_GAHELPERFORBP_API UKM_GAHelperFunctions : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
	UFUNCTION(BlueprintCallable, meta = (DefaultToSelf = "Target"), Category = "KM_GAHelper")
	static void SetupAbilitySystem(AActor* Target, UAbilitySystemComponent* AbilitySystem, TArray<TSubclassOf<class UGameplayAbility>> AbilityList);
	UFUNCTION(BlueprintCallable, meta = (DefaultToSelf = "Target"), Category = "KM_GAHelper")
	static void InitAbilitySystem(AActor* Target, UAbilitySystemComponent* AbilitySystem);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void RefreshAbilityActorInfo(UAbilitySystemComponent* AbilitySystem);
	UFUNCTION(BlueprintCallable, meta = (DefaultToSelf = "Ability"), Category = "KM_GAHelper")
	static void AddGameplayTags(UGameplayAbility* Ability, const FGameplayTagContainer GameplayTags);
	UFUNCTION(BlueprintCallable, meta = (DefaultToSelf = "Ability"), Category = "KM_GAHelper")
	static void RemoveGameplayTags(UGameplayAbility* Ability, const FGameplayTagContainer GameplayTags);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper", meta = (DeterminesOutputType = "Attributes", DynamicOutputParam = "OutAttribute"))
	static void InitAttributeSet(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UAttributeSet> Attributes, UAttributeSet*& OutAttribute);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void SetReplicationModeFull(UAbilitySystemComponent* AbilitySystem);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void SetReplicationModeMixed(UAbilitySystemComponent* AbilitySystem);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void SetReplicationModeMinimal(UAbilitySystemComponent* AbilitySystem);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void GetAbilityLevel(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UGameplayAbility> Class, int& Level);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void SetAbilityLevel(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UGameplayAbility> Class, int Level);
	UFUNCTION(BlueprintCallable, Category = "KM_GAHelper")
	static void IncrementAbilityLevel(UAbilitySystemComponent* AbilitySystem, TSubclassOf<class UGameplayAbility> Class);
};
