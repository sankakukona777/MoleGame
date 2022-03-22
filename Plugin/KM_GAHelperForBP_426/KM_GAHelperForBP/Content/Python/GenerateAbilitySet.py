import unreal
import shutil
import sys
import os
import subprocess

header_dir = unreal.SystemLibrary.get_project_directory() + "Source/" + unreal.SystemLibrary.get_game_name() + "/Public/KM_Generated/"
source_dir = unreal.SystemLibrary.get_project_directory() + "Source/" + unreal.SystemLibrary.get_game_name() + "/Private/KM_Generated/"
if os.path.exists(header_dir) == False:
	os.makedirs(header_dir)
if os.path.exists(source_dir) == False:
	os.makedirs(source_dir)

ability_set_header_content = """
// Fill out your copyright notice in the Description page of Project Settings.
#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "Templates/SubclassOf.h"
#include "Engine/DataAsset.h"
#include "Abilities/GameplayAbility.h"
#include "EKM_GameplayAbilityInputBinds.h"
#include "KM_GameplayAbilitySet.generated.h"

class UAbilitySystemComponent;

USTRUCT()
struct FKM_GameplayAbilityBindInfo
{{
	GENERATED_USTRUCT_BODY()

	UPROPERTY(EditAnywhere, Category = BindInfo)
	EKM_GameplayAbilityInputBinds Command = EKM_GameplayAbilityInputBinds::None;

	UPROPERTY(EditAnywhere, Category = BindInfo)
	TSubclassOf<UGameplayAbility>	GameplayAbilityClass;
}};

UCLASS(BlueprintType, Blueprintable)
class {}_API UKM_GameplayAbilitySet : public UPrimaryDataAsset
{{
	GENERATED_UCLASS_BODY()

	UPROPERTY(EditAnywhere, Category = AbilitySet)
	TArray<FKM_GameplayAbilityBindInfo>	Abilities;

	UFUNCTION(BlueprintCallable, Category = KM_GAHelper)
	void GiveAbilities(UAbilitySystemComponent* AbilitySystemComponent, AActor* Actor) const;
}};
"""

ability_set_header_path = header_dir + "KM_GameplayAbilitySet.h"
ability_set_header_file = open(ability_set_header_path, "w")
ability_set_header_file.write(ability_set_header_content.format(unreal.SystemLibrary.get_game_name().upper()))
ability_set_header_file.close()

ability_set_source_content = """
// Fill out your copyright notice in the Description page of Project Settings.

#include "KM_Generated/KM_GameplayAbilitySet.h"
#include "AbilitySystemComponent.h"

UKM_GameplayAbilitySet::UKM_GameplayAbilitySet(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{

}

void UKM_GameplayAbilitySet::GiveAbilities(UAbilitySystemComponent* AbilitySystemComponent, AActor* Actor) const
{
	for (const FKM_GameplayAbilityBindInfo& BindInfo : Abilities)
	{
		if (BindInfo.GameplayAbilityClass)
		{
			AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(BindInfo.GameplayAbilityClass, 1, (int32)BindInfo.Command));
		}
	}
	AbilitySystemComponent->BindAbilityActivationToInputComponent(Actor->InputComponent,
		FGameplayAbilityInputBinds(FString(""), FString(""), FString("EKM_GameplayAbilityInputBinds")));
}
"""
ability_set_source_path = source_dir + "KM_GameplayAbilitySet.cpp"
ability_set_source_file = open(ability_set_source_path, "w")
ability_set_source_file.write(ability_set_source_content)
ability_set_source_file.close()

mapping = unreal.InputSettings.get_input_settings().get_action_names()
print(mapping)

enum_header_content = """
// Fill out your copyright notice in the Description page of Project Settings.
#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"

UENUM(BlueprintType)
enum class EKM_GameplayAbilityInputBinds : uint8
{{
	None,
{actions}
}};
"""

actions = ""

for action_index, action_name in enumerate(mapping):
	actions = actions + "	" + str(action_name) + ",\n"

enum_header_content_merged = enum_header_content.format(actions=actions)
enum_header_path = header_dir + "EKM_GameplayAbilityInputBinds.h"
enum_header_file = open(enum_header_path, "w")
enum_header_file.write(enum_header_content_merged)
enum_header_file.close()

build_tool = unreal.Paths.engine_dir() + "/Binaries/DotNET/UnrealBuildTool.exe"
if os.path.exists(build_tool) == False:
	build_tool = unreal.Paths.engine_dir() + "/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.exe"

process_string = build_tool + " -projectfiles -project=" + unreal.Paths.get_project_file_path() + " -game -rocket -progress"
subprocess.call(process_string)
